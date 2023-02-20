import os
from get_file import list_dir
from merkleTree import creatMerkleTree, merkleTreeNode, verifyTree, show_value
from RSA import sign, verifySign


# 创建根节点
def get_root(p):
    all_file = list_dir(p)
    nodes = []
    for data in all_file:
        nodes.append(merkleTreeNode(data=data['content'], title=data['title']))
    r = creatMerkleTree(nodes)
    return r


# 展示节点的hash值
def show(r):
    show_value(r)


def get_compare(root):
    while True:
        path = input('请输入文件路径：\n')
        if os.path.exists(path):
            break
        else:
            print('文件路径不存在，请重新输入')
    root1 = get_root(path)
    # 指定源文件的路径
    while True:
        flag = input('请输入选择: 1.展示文件hash值 2.验证文件是否被损坏 3.退出\n')
        if flag == '1':
            print('源文件的hash值')
            show(root)
            print('当前文件hash值: ')
            show(root1)
        elif flag == '2':
            errors = verifyTree(root, root1)
            if errors:
                for error in errors:
                    print('错误信息:', error)
            else:
                print('文件没有损坏')
        else:
            break


if __name__ == '__main__':
    root = get_root('origin')
    signature = sign(root.data)
    print('源文件的数字签名内容以及根节点的hash值如下所示:\n' + '数字签名:\n' + signature.hex() + '\n根节点值: ' + root.data)
    print('现在开始验证签名是否有效!!')
    public_key_path = input('请输入公钥路径(RSA_key/public_key.pem):\n')
    if verifySign(root.data, signature, public_key_path):
        get_compare(root)
    else:
        print('请寻找正确的源文件比对!!')
