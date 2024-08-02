import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tuma_ai",
    version="1.1",
    author="Tangyuqi",
    url='https://gitee.com/tangyuqi-code/tuma-ai',
    author_email="644853320@qq.com",
    description="适合编程教学学习使用的AI库",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
