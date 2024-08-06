from setuptools import setup

readme = "./ReadMe.md"

setup(name='Mtripix',
      version='0.0.7',
      description="api handle for data transform",
      long_description=open(readme, encoding='utf-8').read(),
      long_description_content_type='text/markdown',
      author='TriplePixels',
      author_email='PIPIPINoBrain@163.com',
      requires=['numpy', 'json', 'lxml', 'PIL', 'imgviz'],  # 定义依赖哪些模块
      #packages=find_packages(),  # 系统自动从当前目录开始找包
      # 如果有的文件不用打包，则只能指定需要打包的文件
      packages=['Mtripix'],  #指定目录中需要打包的py文件，注意不要.py后缀
      license="apache 3.0"
      )