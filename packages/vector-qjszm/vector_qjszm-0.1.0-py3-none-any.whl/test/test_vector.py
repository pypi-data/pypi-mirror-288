import unittest
from vector import Vector

class TestVector(unittest.TestCase):
    def test_init(self):
        v = Vector()
        self.assertEqual(v.x, 0)
        self.assertEqual(v.y, 0)

        v = Vector(1, 2)
        self.assertEqual(v.x, 1)
        self.assertEqual(v.y, 2)

    def test_add(self):
        v1 = Vector(1, 2)
        v2 = Vector(2, 1)
        v3 = v1 + v2
        self.assertEqual(v3.x, 3)
        self.assertEqual(v3.y, 3)    

    def test_neg(self):
        v1 = Vector(1, 2)
        v2 = -v1
        self.assertEqual(v2.x, -1)
        self.assertEqual(v2.y, -2)

    def test_sub(self):
        v1 = Vector(1, 2)
        v2 = Vector(2, 1)
        v3 = v1 - v2
        self.assertEqual(v3.x, -1)
        self.assertEqual(v3.y, 1)

    def test_norm(self):
        v1 = Vector(3, 4)
        self.assertAlmostEqual(v1.norm, 5, places=5)

    def test_mul(self):
        v1 = Vector(1, 2)
        v2 = v1 * 2
        self.assertEqual(v2.x, 2)
        self.assertEqual(v2.y, 4)

    def test_rmul(self):
        v1 = Vector(1, 2)
        v2 = 2 * v1
        self.assertEqual(v2.x, 2)
        self.assertEqual(v2.y, 4)

    def test_dot(self):
        v1 = Vector(1, 2)
        v2 = Vector(2, 1)
        self.assertEqual(v1.dot(v2), 4)

    def test_eq_same_vector(self):
        """
        测试两个相同向量的相等性
        """
        v1 = Vector(1, 2)
        v2 = Vector(1, 2)
        self.assertTrue(v1 == v2)

    def test_unit(self):
        # 测试非零向量的单位向量
        v1 = Vector(3, 4)
        unit_v1 = v1.unit()
        self.assertAlmostEqual(unit_v1._x, 0.6)
        self.assertAlmostEqual(unit_v1._y, 0.8)

        # 测试零向量
        v2 = Vector(0, 0)
        with self.assertRaises(ValueError):
            v2.unit()

    def test_eq_different_vectors(self):
        """
        测试两个不同向量的相等性
        """
        v1 = Vector(1, 2)
        v2 = Vector(3, 4)
        self.assertFalse(v1 == v2)

    def test_eq_invalid_other_type(self):
        """
        测试与非向量类型进行相等性比较
        """
        v1 = Vector(1, 2)
        other = 5
        with self.assertRaises(AssertionError):
            v1 == other