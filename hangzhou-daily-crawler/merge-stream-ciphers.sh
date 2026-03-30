#!/bin/bash
# 合并流密码翻译三部分文件并提交

set -e

cd /root/.openclaw/workspace/book

# 检查 pt2 和 pt3 文件是否存在，如果不在 src 下，则在当前目录
if [ -f "src/stream-ciphers-pt2.rst" ]; then
    PART2="src/stream-ciphers-pt2.rst"
elif [ -f "stream-ciphers-pt2.rst" ]; then
    PART2="stream-ciphers-pt2.rst"
else
    echo "错误：找不到 part2 文件"
    exit 1
fi

if [ -f "src/stream-ciphers-pt3.rst" ]; then
    PART3="src/stream-ciphers-pt3.rst"
elif [ -f "stream-ciphers-pt3.rst" ]; then
    PART3="stream-ciphers-pt3.rst"
else
    echo "错误：找不到 part3 文件"
    exit 1
fi

# 临时合并文件
cat > src/stream-ciphers.rst << 'EOF'
流密码
------
.. _description-2:

描述
~~~~

:term:`流密码` 是一种 :term:`对称密钥加密` 算法，它加密位的流。
理想情况下，该流可以任意长；实际的 :term:`流密码`\s 有限制，但它们
通常足够大，不会造成实际问题。
EOF

# 提取第一部分 (head -n 655)，跳过开头的标题行（已在上面的cat中添加）
git show zh_CN-translation:src/stream-ciphers.rst | tail -n +3 > /tmp/part1.tmp

# 提取第二部分和第三部分
cat "$PART2" > /tmp/part2.tmp
cat "$PART3" > /tmp/part3.tmp

# 合并三个部分
cat /tmp/part1.tmp > src/stream-ciphers.rst
echo "" >> src/stream-ciphers.rst
cat /tmp/part2.tmp >> src/stream-ciphers.rst
echo "" >> src/stream-ciphers.rst
cat /tmp/part3.tmp >> src/stream-ciphers.rst

# 合并三个部分
cat /tmp/part1.tmp > src/stream-ciphers.rst
echo "" >> src/stream-ciphers.rst
cat /tmp/part2.tmp >> src/stream-ciphers.rst
echo "" >> src/stream-ciphers.rst
cat /tmp/part3.tmp >> src/stream-ciphers.rst

# 清理临时文件
rm -f /tmp/part*.tmp src/stream-ciphers-pt*.rst

# 验证行数
echo "合并后文件行数: $(wc -l < src/stream-ciphers.rst)"
echo "应接近: $(git show master:src/stream-ciphers.rst | wc -l)"

# Git 操作
git add src/stream-ciphers.rst
git status --short

# 提交（如果当前在 zh_CN-translation 分支）
branch=$(git branch --show-current)
if [ "$branch" = "zh_CN-translation" ]; then
    git commit -m "zh_CN: translate stream-ciphers.rst (part 2/3 and part 3/3) - complete"
    git push origin zh_CN-translation
    echo "已提交并推送到 GitHub"
else
    echo "警告：当前不在 zh_CN-translation 分支 (当前: $branch)"
    echo "请切换到该分支后手动提交"
fi
