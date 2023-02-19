import copy
import hashlib
from collections import deque


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
    def encrypt(self, text):
        # 如果当前的内容是空值，我们把文件名增加到内容中去
        if text is None:
            text += self.title
        hash256 = hashlib.sha256()
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
        while nodeNum % 2 == 1:
            # 这里追加尾部的节点
            dup = copy.deepcopy(r[-1:])
            # 将添加节点的是否为添加值设为True
            dup[0].dup = True
            r.extend(dup)
            nodeNum = len(r)
        else:
            # 存放上一层节点
            secondNodes = []
            flag = 0
            while flag < nodeNum:
                newNode = merkleTreeNode(left=r[flag], right=r[flag + 1],
                                         data=r[flag].data + r[flag + 1].data)
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
                if cur.left:
                    if not cur.left.dup:
                        dq.append(cur.left)
                if cur.right:
                    if not cur.right.dup:
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
            print(b.data)


def verifyTree(root1, root2):
    list1 = level_order_traversal(root1)
    list2 = level_order_traversal(root2)
    # 错误列表来存储错误的文件信息
    error_list = []
    if list1[0][0].data == list2[0][0].data:
        return error_list
    size = len(list1[len(list1) - 1])
    # 我们直接到叶子节点获取错误信息
    for i in range(size):
        if list1[len(list1) - 1][i].data == list2[len(list1) - 1][i].data:
            pass
        else:
            error_list.append(list1[len(list1) - 1][i].title + '-->' + list2[len(list1) - 1][i].title)
    return error_list


if __name__ == '__main__':
    leefData = ['1', '2', '3', '4', '5']
    leefData1 = ['1', '9', '3', '4', '4']
    nodes = []
    nodes1 = []
    for data in leefData:
        nodes.append(merkleTreeNode(data=data, title=data))
    for data in leefData1:
        nodes1.append(merkleTreeNode(data=data, title=data))
    root = creatMerkleTree(nodes)
    root1 = creatMerkleTree(nodes1)
    print(verifyTree(root, root1))
    show_value(root)
