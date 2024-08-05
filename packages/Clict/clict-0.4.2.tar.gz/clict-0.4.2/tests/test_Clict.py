#!/usr/bin/env python
import unittest
from Clict import Clict


class TestClict(unittest.TestCase):

	def test_init_with_dict(s):
		c = Clict(a=1, b=2)
		s.assertEqual(c['a'], 1)
		s.assertEqual(c['b'], 2)

	def test_set_get_item(s):
		c = Clict()
		c['a'] = 1
		s.assertEqual(c['a'], 1)

	def test_set_get_attr(s):
		c = Clict()
		c.a = 1
		s.assertEqual(c.a, 1)

	def test_missing_key(s):
		c = Clict()
		# s.assertIsInstance(c['missing'], Clict)
		s.assertIsInstance(c.missing, Clict)

	def test_contains_key(s):
		c = Clict(a=1)
		s.assertIn('a', c)
		s.assertNotIn('b', c)

	def test_keys(s):
		c = Clict(a=1, b=2)
		s.assertListEqual(list(c.keys()), ['a', 'b'])

	def test_items(s):
		c = Clict(a=1, b=2)
		s.assertDictEqual(c.items(), {'a': 1, 'b': 2})

	def test_values(s):
		c = Clict(a=1, b=2)
		s.assertListEqual(c.values(), [1, 2])

	def test_set_parent(s):
		c = Clict()
		c.d.asplit.child='findme'
		c.d.bsplit.child='fromhere'
		# localparent=c.d.__setparent__('iamparent')
		s.assertEqual(c.d.bsplit.__getparent__()().asplit.child,'findme')

	def test_str(s):
		c = Clict(a=1, b=2)
		s.assertIsInstance(str(c), str)



	def test_fromdict(s):
		c = Clict()
		c.__fromdict__({'a': {'b': 2}})
		s.assertIsInstance(c['a'], Clict)
		s.assertEqual(c['a']['b'], 2)
	def test_fromlist(s):
		c = Clict()
		c.__fromlist__(['a','b'])
		s.assertEqual(c[0], 'a')
		s.assertEqual(c[1], 'b')
		c=Clict(['a','b'])
		s.assertEqual(c[0], 'a')
		s.assertEqual(c[1], 'b')
		s.assertEqual(c._1, 'b')
		c=Clict(mylist=['a','b'])
		s.assertEqual(c.mylist[0], 'a')
		c.mylist[2]='c'
		s.assertEqual(c.mylist._2, 'c')
	def test_printcolor(s):
		c=Clict(['a','b'],c=['d',{'e':'f'}])
		print(c)
	def test_printfancy(s):
		c=Clict(['a','b'],g=['d',{'e':'f'}])
		c.p.q.r.s.t.u.v.w.x.y='test'
		print(repr(c))


if __name__ == '__main__':
	unittest.main()
