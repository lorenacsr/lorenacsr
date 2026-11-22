"""ETL demonstrativo reproduzível. Python 3.10+, apenas biblioteca padrão."""
from pathlib import Path
from datetime import date, timedelta
from collections import Counter
import argparse
import csv
import hashlib
import json
import random
import sqlite3

ROOT = Path(__file__).resolve().parents[1]
CUTOFF = date(2026, 11, 22)


def save_csv(path, rows, fields=None):
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = list(rows)
    with path.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fields or list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path):
    with path.open(encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f))


def deadline(start, days, mode, closed=(), adjust=True):
    """Exclui início; calendário demonstrativo, sem presumir feriados reais."""
    if mode not in ('corridos', 'uteis') or days < 1:
        raise ValueError('Regra de prazo não validada')
    closed = set(closed)
    def working(d):
        return d.weekday() < 5 and d not in closed
    result = start
    count = 0
    while count < days:
        result += timedelta(days=1)
        if mode == 'corridos' or working(result):
            count += 1
    while adjust and not working(result):
        result += timedelta(days=1)
    return result


def generate():
    """Somente dados fictícios; não reescreve dados no comando run."""
    rng = random.Random(42)
    raw = ROOT / 'data/raw'
    units = [{'unidade_id': f'U{i}', 'unidade': f'Unidade fictícia {i}'} for i in range(1, 5)]
    items = [{'item_id': f'M{i}', 'item': f'Medicamento simulado {i}', 'unidade_medida': 'comprimido'} for i in range(1, 6)]
    suppliers = [{'fornecedor_id': f'F{i}', 'fornecedor': f'Fornecedor fictício {i}'} for i in range(1, 4)]
    contracts = [dict(contrato_id=f'C{i}', fornecedor_id=f'F{i}', prazo_dias=15,
                      tipo_dias='corridos', marco='envio_af', regra_validada=1,
                      ajustar_vencimento=1, fundamento='Cláusula fictícia para demonstração; não é contrato municipal')
                 for i in range(1, 4)]
    save_csv(raw / 'unidades.csv', units)
    save_csv(raw / 'itens.csv', items)
    save_csv(raw / 'fornecedores.csv', suppliers)
    save_csv(raw / 'contratos.csv', contracts)
    save_csv(raw / 'calendario.csv', [{'data': '2026-10-12', 'motivo': 'Fechamento fictício do órgão para teste'}])
    demands, orders, deliveries = [], [], []
    for month in range(1, 11):
        for unit in units:
            for item in items:
                planned = rng.randrange(80, 181, 10)
                requested = round(planned * rng.choice([0.8, 1, 1, 1.15, 1.4, 1.8]))
                demands.append(dict(demanda_id=f'D{len(demands)+1:04}', competencia=f'2026-{month:02}-01',
                                    unidade_id=unit['unidade_id'], item_id=item['item_id'],
                                    planejado=planned, solicitado=requested))
        for item in items:
            idx = len(orders) + 1
            issued = date(2026, month, 2)
            quantity = sum(d['solicitado'] for d in demands if d['competencia'] == f'2026-{month:02}-01' and d['item_id'] == item['item_id'])
            orders.append(dict(af_item_id=f'AF{idx:03}', contrato_id=f'C{(idx%3)+1}', item_id=item['item_id'],
                               data_envio=issued.isoformat(), quantidade=str(quantity), preco_centavos=22+idx%80))
            case = idx % 5
            if case == 0:  # pendente sem entrega
                continue
            first = quantity // 2 if case in (2, 3) else quantity
            deliveries.append(dict(entrega_id=f'E{idx:03}A', af_item_id=f'AF{idx:03}',
                                   data_entrega=(issued+timedelta(days=10 if case != 4 else 24)).isoformat(), quantidade=first))
            if case == 2:
                deliveries.append(dict(entrega_id=f'E{idx:03}B', af_item_id=f'AF{idx:03}',
                                       data_entrega=(issued+timedelta(days=22)).isoformat(), quantidade=quantity-first))
    # Anomalias controladas: duplicata exata, espaços/caixa, quantidade inválida,
    # referência inexistente e conflito no mesmo identificador.
    demands.append(demands[0].copy())
    demands[1]['unidade_id'] = ' u1 '
    invalid = demands[2].copy(); invalid.update(demanda_id='D_ERRO', solicitado=-9); demands.append(invalid)
    missing = demands[3].copy(); missing.update(demanda_id='D_REF', unidade_id='U99'); demands.append(missing)
    conflict = orders[0].copy(); conflict.update(af_item_id='AF_CONFLITO'); orders.append(conflict)
    conflict2 = conflict.copy(); conflict2['quantidade'] = '999'; orders.append(conflict2)
    save_csv(raw / 'demandas.csv', demands)
    save_csv(raw / 'af_itens.csv', orders)
    save_csv(raw / 'entregas.csv', deliveries)


def deduplicate(rows, key, audit, source):
    """Remove cópia exata; rejeita TODAS as versões de chave conflitante."""
    seen, unique = set(), []
    for line, row in enumerate(rows, 2):
        signature = tuple(row.items())
        if signature in seen:
            audit.append(dict(fonte=source, linha=line, chave=row[key], acao='duplicata_removida', motivo='Registro idêntico'))
        else:
            seen.add(signature); unique.append((line, row))
    counts = Counter(row[key] for _, row in unique)
    result = []
    for line, row in unique:
        if counts[row[key]] > 1:
            audit.append(dict(fonte=source, linha=line, chave=row[key], acao='rejeitado', motivo='Chave com versões conflitantes'))
        else:
            result.append((line, row))
    return result


def run(cutoff=CUTOFF):
    out = ROOT / 'data/processed'; out.mkdir(parents=True, exist_ok=True)
    reports = ROOT / 'reports'; reports.mkdir(exist_ok=True)
    audit = []
    db = sqlite3.connect(':memory:')
    db.row_factory = sqlite3.Row
    db.executescript((ROOT / 'sql/schema.sql').read_text())
    for name in ('unidades', 'itens', 'fornecedores', 'contratos'):
        rows = read_csv(ROOT / f'data/raw/{name}.csv')
        for row in rows:
            db.execute(f"INSERT INTO {name} ({','.join(row)}) VALUES ({','.join('?' for _ in row)})", tuple(row.values()))
    unit_ids = {r[0] for r in db.execute('SELECT unidade_id FROM unidades')}
    item_ids = {r[0] for r in db.execute('SELECT item_id FROM itens')}
    contract_ids = {r[0] for r in db.execute('SELECT contrato_id FROM contratos')}
    keys = {'demandas': 'demanda_id', 'af_itens': 'af_item_id', 'entregas': 'entrega_id'}
    metrics = {}
    for name, key in keys.items():
        raw = read_csv(ROOT / f'data/raw/{name}.csv')
        metrics[name] = {'entrada': len(raw)}
        clean = []
        for line, row in deduplicate(raw, key, audit, name):
            try:
                for field in ('unidade_id', 'item_id', 'contrato_id', 'af_item_id'):
                    if field in row:
                        normalized = row[field].strip().upper()
                        if normalized != row[field]:
                            audit.append(dict(fonte=name, linha=line, chave=row[key], acao='padronizado', motivo=f'{field}: espaços/caixa'))
                        row[field] = normalized
                if name == 'demandas':
                    assert row['unidade_id'] in unit_ids and row['item_id'] in item_ids, 'Referência inexistente'
                    for field in ('planejado', 'solicitado'):
                        row[field] = int(row[field]); assert row[field] >= 0, 'Quantidade negativa'
                    d = date.fromisoformat(row['competencia']); assert d.day == 1 and d <= cutoff, 'Competência inválida/futura'
                elif name == 'af_itens':
                    assert row['contrato_id'] in contract_ids and row['item_id'] in item_ids, 'Referência inexistente'
                    row['quantidade'] = int(row['quantidade']); row['preco_centavos'] = int(row['preco_centavos'])
                    assert row['quantidade'] > 0 and row['preco_centavos'] >= 0, 'Quantidade/preço inválido'
                    assert date.fromisoformat(row['data_envio']) <= cutoff, 'Envio futuro'
                else:
                    af = db.execute('SELECT * FROM af_itens WHERE af_item_id=?', (row['af_item_id'],)).fetchone()
                    assert af is not None, 'AF inexistente'
                    row['quantidade'] = int(row['quantidade']); assert row['quantidade'] > 0, 'Quantidade inválida'
                    assert date.fromisoformat(af['data_envio']) <= date.fromisoformat(row['data_entrega']) <= cutoff, 'Data de entrega inválida/futura'
                clean.append(row)
            except (AssertionError, ValueError) as exc:
                audit.append(dict(fonte=name, linha=line, chave=row[key], acao='rejeitado', motivo=str(exc)))
        # Evita dupla contagem de demanda agregada mesmo com IDs diferentes.
        if name == 'demandas':
            counts = Counter((r['competencia'],r['unidade_id'],r['item_id']) for r in clean)
            valid = []
            for r in clean:
                if counts[(r['competencia'],r['unidade_id'],r['item_id'])] > 1:
                    audit.append(dict(fonte=name, linha=0, chave=r[key], acao='rejeitado', motivo='Grão de demanda conflitante'))
                else: valid.append(r)
            clean = valid
        # Se entregas excedem o pedido, rejeita o conjunto da AF para revisão.
        if name == 'entregas':
            totals = Counter()
            for r in clean: totals[r['af_item_id']] += r['quantidade']
            bad = {k for k,v in totals.items() if v > db.execute('SELECT quantidade FROM af_itens WHERE af_item_id=?',(k,)).fetchone()[0]}
            valid = []
            for r in clean:
                if r['af_item_id'] in bad:
                    audit.append(dict(fonte=name, linha=0, chave=r[key], acao='rejeitado', motivo='Entregas excedem quantidade da AF; revisar conjunto'))
                else: valid.append(r)
            clean = valid
        for row in clean:
            db.execute(f"INSERT INTO {name} ({','.join(row)}) VALUES ({','.join('?' for _ in row)})", tuple(row.values()))
        metrics[name]['aceitos'] = len(clean)
        metrics[name]['duplicatas'] = sum(a['fonte']==name and a['acao']=='duplicata_removida' for a in audit)
        metrics[name]['rejeitados'] = sum(a['fonte']==name and a['acao']=='rejeitado' for a in audit)
        assert metrics[name]['entrada'] == metrics[name]['aceitos'] + metrics[name]['duplicatas'] + metrics[name]['rejeitados']
    closed = {date.fromisoformat(r['data']) for r in read_csv(ROOT / 'data/raw/calendario.csv')}
    for af in db.execute('SELECT a.*, c.prazo_dias,c.tipo_dias,c.regra_validada,c.ajustar_vencimento FROM af_itens a JOIN contratos c USING(contrato_id)').fetchall():
        due = None
        if af['regra_validada'] and af['tipo_dias'] in ('corridos','uteis'):
            due = deadline(date.fromisoformat(af['data_envio']),af['prazo_dias'],af['tipo_dias'],closed,bool(af['ajustar_vencimento'])).isoformat()
        db.execute('UPDATE af_itens SET data_limite=? WHERE af_item_id=?', (due, af['af_item_id']))
    db.execute('INSERT INTO parametros VALUES (?)',(cutoff.isoformat(),))
    db.executescript((ROOT / 'sql/analises.sql').read_text())
    for table in ('unidades','itens','fornecedores','contratos','demandas','af_itens','entregas','vw_demanda','vw_entregas','vw_fornecedores'):
        cursor = db.execute(f'SELECT * FROM {table}')
        save_csv(out / f'{table}.csv', [dict(r) for r in cursor.fetchall()], [c[0] for c in cursor.description])
    save_csv(reports / 'qualidade.csv', audit, ['fonte','linha','chave','acao','motivo'])
    totals = dict(db.execute('SELECT SUM(quantidade) pedido, SUM(entregue) entregue, SUM(pendente) pendente, SUM(valor_pendente_centavos) valor_pendente_centavos FROM vw_entregas').fetchone())
    assert totals['pedido'] == totals['entregue'] + totals['pendente']
    metrics['totais'] = totals
    metrics['data_corte'] = cutoff.isoformat()
    metrics['origem'] = 'Dados inteiramente simulados; regras contratuais fictícias'
    metrics['sha256_entradas'] = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((ROOT / 'data/raw').glob('*.csv'))}
    (reports / 'execucao.json').write_text(json.dumps(metrics, ensure_ascii=False, indent=2)+'\n')
    dest = sqlite3.connect(out / 'compras.sqlite'); db.backup(dest); dest.close(); db.close()
    print(json.dumps(metrics, ensure_ascii=False, indent=2))
    return metrics


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['generate','run'])
    parser.add_argument('--data-corte', default=CUTOFF.isoformat())
    args = parser.parse_args()
    if args.action == 'generate': generate()
    else: run(date.fromisoformat(args.data_corte))
