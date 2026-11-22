import sys
import unittest
from datetime import date
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from pipeline import deadline, deduplicate, run

class Rules(unittest.TestCase):
    def test_excludes_start_includes_due(self):
        self.assertEqual(deadline(date(2026,11,2),15,'corridos'), date(2026,11,17))
    def test_weekend_and_local_closure(self):
        # 15º dia sábado; segunda fechada => terça, sem apagar vencimento original na documentação.
        self.assertEqual(deadline(date(2026,10,23),15,'corridos',{date(2026,11,9)}),date(2026,11,10))
    def test_business_days(self):
        self.assertEqual(deadline(date(2026,11,6),1,'uteis',{date(2026,11,9)}),date(2026,11,10))
    def test_undefined_rule_is_not_guessed(self):
        with self.assertRaises(ValueError): deadline(date(2026,11,2),15,'indefinido')
    def test_conflict_does_not_keep_arbitrary_version(self):
        audit=[]
        out=deduplicate([{'id':'A','q':'1'},{'id':'A','q':'1'},{'id':'A','q':'2'},{'id':'B','q':'3'}],'id',audit,'teste')
        self.assertEqual([r['id'] for _,r in out],['B'])
        self.assertEqual(len(audit),3)
    def test_reconciliation_and_partial_deliveries(self):
        metrics=run()
        self.assertEqual(metrics['demandas']['aceitos'],200)
        self.assertEqual(metrics['demandas']['duplicatas'],1)
        self.assertEqual(metrics['demandas']['rejeitados'],2)
        self.assertEqual(metrics['af_itens']['rejeitados'],2)
        t=metrics['totais']; self.assertEqual(t['pedido'],t['entregue']+t['pendente'])
        import sqlite3
        with sqlite3.connect(Path(__file__).resolve().parents[1]/'data/processed/compras.sqlite') as db:
            # AF002 tem duas parcelas. Pedido não pode dobrar no JOIN.
            row=db.execute("SELECT quantidade,entregue,pendente,situacao FROM vw_entregas WHERE af_item_id='AF002'").fetchone()
            self.assertEqual(row[0],row[1]); self.assertEqual(row[2],0)
            self.assertEqual(row[3],'concluido_com_atraso')
            self.assertEqual(db.execute('PRAGMA foreign_key_check').fetchall(),[])

if __name__=='__main__': unittest.main()
