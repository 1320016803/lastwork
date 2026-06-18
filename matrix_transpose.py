import numpy as np
mat = np.array([[2, 1, 0],
                [1, 2, 1],
                [0, 1, 2]])

print("=" * 40)
print("方法一：NumPy 转置")
print("=" * 40)
print("原矩阵：")
print(mat)
print("\n转置矩阵 (mat.T)：")
print(mat.T)
print("\n转置矩阵 (mat.transpose())：")
print(mat.transpose())
print("\n转置矩阵 (np.transpose(mat))：")
print(np.transpose(mat))