from collections import deque
import os


# 该函数可以返回一个生成器对象，从而达到节省空间的效果
def BFS(root):
    if not root:
        return
    q = deque()
    q.append(root)
    while q:
        size = len(q)
        for i in range(size):
            node = q.popleft()
            if node.left and not node.dup:
                q.append(node.left)
            if node.right and not node.dup:
                q.append(node.right)
            yield node


# 该函数可以返回叶子节点，并且这个函数也是一个生成器函数
def find_leaves(root):
    if root is None:
        return
    if root.left is None and root.right is None:
        yield root
    yield from find_leaves(root.left)
    yield from find_leaves(root.right)


# 改良后的判断文件完整性函数
def verityTree_improve_version(r1, r2):
    error_list = []
    if r1.data == r2.data:
        return error_list
    list1 = list(find_leaves(r1))
    list2 = list(find_leaves(r2))
    size1 = len(list1)
    size2 = len(list2)

    # 使用os来取文件名
    set1 = set(os.path.basename(d.title) for d in list1)
    set2 = set(os.path.basename(d.title) for d in list2)

    if size1 > size2:
        diff = set1.symmetric_difference(set2)
        list1 = [d for d in list1 if os.path.basename(d.title) not in diff]
        for di in diff:
            error_list.append('在下载文件中缺失' + di)
    # 处理多余文件的情况
    elif size1 < size2:
        diff = set2.symmetric_difference(set1)
        list2 = [d for d in list1 if os.path.basename(d.title) not in diff]
        for di in diff:
            error_list.append('在源文件中不存在' + di)
    # 处理文件冲突的情况
    else:
        diff = set1.symmetric_difference(set2)
        list1 = [d for d in list1 if os.path.basename(d.title) not in diff]
        list2 = [d for d in list2 if os.path.basename(d.title) not in diff]
        for di in diff:
            error_list.append('发生文件冲突' + di + '不存在或多余')
    # 遍历叶子节点，逐个比较它们的hash值
    for i in range(len(list1)):
        if list1[i].data == list2[i].data:
            continue
        error_list.append(f"{list1[i].title} --> {list2[i].title}")
    return error_list


