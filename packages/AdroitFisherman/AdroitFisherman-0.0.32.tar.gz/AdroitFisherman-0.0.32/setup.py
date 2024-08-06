from setuptools import setup,Extension
SeqList=Extension("AdroitFisherman.SequentialList",sources=['AdroitFisherman/includes/List/SequentialList/SeqList.c'])
SingleLinkedList=Extension("AdroitFisherman.SingleLinkedList",sources=['AdroitFisherman/includes/List/SingleLinkedList/SingleLinkedList.c'])
SingleLinkedListWithoutHeadNode=Extension("AdroitFisherman.SingleLinkedListWithoutHeadNode",sources=['AdroitFisherman/includes/List/SingleLinkedListWithoutHeadNode/SingleLinkedListWithoutHeadNode.c'])
CircularSingleLinkedList=Extension("AdroitFisherman.CircularSingleLinkedList",sources=['AdroitFisherman/includes/List/CircularSingleLinkedList/CircularSingleLinkedList.c'])
DoubleLinkedList=Extension("AdroitFisherman.DoubleLinkedList",sources=['AdroitFisherman/includes/List/DoubleLinkedList/DoubleLinkedList.c'])
Base64=Extension("AdroitFisherman.Base64Utility",sources=['AdroitFisherman/includes/Base/Base64Util.c'])
LinkedStack=Extension("AdroitFisherman.LinkedStack",sources=['AdroitFisherman/includes/LinkedStack/LinkedStack.c'])
SHA512=Extension("AdroitFisherman.SHAUtility",sources=['AdroitFisherman/includes/SHA/SHA512.c'])
read_me = open('README.md', 'r',encoding='utf-8')
setup(
    name="AdroitFisherman",
    version="0.0.32",
    author="adroit_fisherman",
    author_email="1295284735@qq.com",
    platforms="Windows",
    description="This is a simple package about Data Structure packed by C/C++ language.",
    long_description_content_type="text/markdown",
    long_description=read_me.read(),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Natural Language :: Chinese (Simplified)",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Operating System :: Microsoft :: Windows :: Windows 11",
        "Programming Language :: C++",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.9",
        "Topic :: Utilities"
    ],
    include_package_data=True,
    packages=['AdroitFisherman.Utilities'],
    ext_modules=[
        SeqList,
        SingleLinkedList,
        SingleLinkedListWithoutHeadNode,
        CircularSingleLinkedList,
        DoubleLinkedList,
        Base64,
        LinkedStack,
        SHA512
    ],
    license="GPL"
)
read_me.close()
