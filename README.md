# Merkle Tree 文件完整性验证工具
# Info
本工具使用 Merkle Tree 算法来验证文件的完整性。Merkle Tree 是一种树形结构，每个叶子节点代表文件块的哈希值，非叶子节点是其子节点的哈希值的哈希值。通过计算根节点的哈希值，可以验证整个文件的完整性。如果文件被篡改，那么计算出来的根节点哈希值将与原始值不同。

# Install
在运行之前，需要安装 Python3 和以下依赖库：


`pip install hashlib os re`


# Usage
1. 输入文件路径</br>
在运行 main.py 后，程序会提示输入要验证的文件夹的路径。可以输入绝对路径或者相对路径。

2. 选择功能
程序会提示输入数字选择功能，支持以下功能：

    展示文件 hash 值</br>
    验证文件是否被篡改</br>
    退出</br>
输入数字后，按回车键执行相应的功能。

3. 输出结果</br>
如果选择展示文件 hash 值，程序会输出源文件和当前文件的哈希值。
如果选择验证文件是否被篡改，程序会输出错误的文件路径，如果没有错误，则输出“文件没有损坏”。

4. 批量处理文件</br>
可以将整个文件夹的文件进行批量验证。只需要将所有要验证的文件放在同一个文件夹内，输入该文件夹的路径即可。

# Warning
本程序只支持对文件的完整性进行验证，不保证文件的安全性。</br>
如果文件路径不存在，程序会报错。</br>
对于大规模模型文件，程序可能会出现效率低下的情况。</br>

# update
新增可以验证图片文件以及svg格式文件功能</br>
以及可以处理文件多余或缺失以及文件冲突（即文件名错误）的情况</br>
优化了merkle树的遍历逻辑以及验证树完整性的逻辑，使用generator来优化函数，达到节约内存的效果</br>
新增RSA数字签名，可以对根节点进行数字签名然后验证根节点的数字签名是否正确