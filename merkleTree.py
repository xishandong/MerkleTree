import copy
import hashlib
from collections import deque
from Cython import typeof


class merkleTreeNode:
    # 初始化树节点
    def __init__(self, left=None, right=None, data=None, title=None):
        # 定义左子树
        self.left = left
        # 定义右子树
        self.right = right
        # 定义存放的hash值
        self.data = self.encrypt(data)
        # 判断是否为补充的节点，默认为False
        self.dup = False
        # 存放当前节点的文件名
        self.title = title

    # 计算节点的hash值
    @staticmethod
    def encrypt(text):
        hash256 = hashlib.sha256()
        if typeof(text) == 'str':
            text = text.encode('utf-8')
        hash256.update(text)
        return hash256.hexdigest()


def creatMerkleTree(r):
    # 计算叶子节点的数量
    nodeNum = len(r)
    # 如果叶子节点为空，直接返回
    if nodeNum == 0:
        return 0
    # 现在处理叶子节点不为0的情况
    else:
        # 如果叶子节点是奇数个，我们需要进行补充
        if nodeNum % 2 == 1:
            # 这里追加尾部的节点
            dup = copy.deepcopy(r[-1:])
            # 将添加节点的是否为添加值设为True
            dup[0].dup = True
            r.extend(dup)
            nodeNum = len(r)
        # 存放上一层节点
        secondNodes = []
        flag = 0
        while flag < nodeNum:
            newNode = merkleTreeNode(left=r[flag], right=r[flag + 1],
                                     data=r[flag].data + r[flag + 1].data,
                                     title='Father_node')
            flag += 2
            secondNodes.append(newNode)
        # 如果现在的上层节点数是一个了，说明到了根结点，返回
        if len(secondNodes) == 1:
            return secondNodes[0]
        # 如果没有，递归调用该函数继续构建树
        else:
            return creatMerkleTree(secondNodes)


def level_order_traversal(r):
    # 准备一个接受所有节点的列表
    results = []
    # 如果是空节点，直接返回空
    if not r:
        return results
    else:
        # 按层次遍历的方式遍历整颗树
        dq = deque([r])
        while dq:
            size = len(dq)
            result = []
            for i in range(size):
                cur = dq.popleft()
                result.append(cur)
                # 我们只取不是填充的节点
                if cur.left and not cur.left.dup:
                    dq.append(cur.left)
                if cur.right and not cur.right.dup:
                    dq.append(cur.right)
            results.append(result)
    return results


def show_value(r):
    # 获取节点列表
    x = level_order_traversal(r)
    i = 1
    for a in x:
        print('第' + str(i) + '层:')
        i += 1
        for b in a:
            print(b.title + '的hash值--> ' + b.data)


def verifyTree(r1, r2):
    list1 = level_order_traversal(r1)
    list2 = level_order_traversal(r2)
    # 错误列表来存储错误的文件信息
    error_list = []
    # 如果两个树的根节点数据相等，则直接返回空的错误列表
    if list1[0][0].data == list2[0][0].data:
        return error_list
    # 获取两棵树的叶子节点数量,并且处理树结构不同的情况，以及两棵树文件名不同的情况
    size1 = len(list1[-1])
    size2 = len(list2[-1])
    set1 = set(d.title.split('/')[-1] for d in list1[-1])
    set2 = set(d.title.split('/')[-1] for d in list2[-1])
    # 处理缺失文件的情况
    if size1 > size2:
        diff = set1.symmetric_difference(set2)
        list1[-1] = [d for d in list1[-1] if d.title.split('/')[-1] not in diff]
        for di in diff:
            error_list.append('在下载文件中缺失' + di)
    # 处理多余文件的情况
    elif size1 < size2:
        diff = set2.symmetric_difference(set1)
        list2[-1] = [d for d in list1[-1] if d.title.split('/')[-1] not in diff]
        for di in diff:
            error_list.append('在源文件中不存在' + di)
    # 处理文件冲突的情况
    else:
        diff = set1.symmetric_difference(set2)
        list1[-1] = [d for d in list1[-1] if d.title.split('/')[-1] not in diff]
        list2[-1] = [d for d in list2[-1] if d.title.split('/')[-1] not in diff]
        for di in diff:
            error_list.append('发生文件冲突' + di + '不存在或多余')
    # 遍历叶子节点，逐个比较它们的hash值
    for i in range(len(list1[-1])):
        if list1[-1][i].data == list2[-1][i].data:
            continue
        error_list.append(f"{list1[-1][i].title} --> {list2[-1][i].title}")
    return error_list

