# TODO

## 跟踪重命名文件

锦上添花。

### GitPython API

`git log`命令的`--follow`和`--find-renames`参数符合需求。 参考：https://www.zhihu.com/question/531483642/answer/2472733253。

目前使用的`Repo.iter_commits`底层基于非常复杂的`git rev-list`命令，超出了我的理解能力，不确定是否可以达到类似的效果。

已经在知乎和GitHub提问。

### 课程平台服务端重新设计

即使可以解决，原本课程平台服务端实现的`lecture_name`相关逻辑也需要改变。目前它是不可变的，文件的重命名被视为新的`lecture_name`。

如果能够定义如何跟踪文件、并设计对应的服务端逻辑，则对`Lecture`的版本更变跟踪可以更加完善。不过暂时不确定是否有明确的使用场景。
