#!/usr/bin/env python
# src/research_crew/main.py
import os
from crewai_ddd_expert.crew import DddExpertCrew

# Create output directory if it doesn't exist
os.makedirs('output', exist_ok=True)

def run():
    """
    Run the DDD Expert Crew.
    """
    inputs = {
        'requirement': '''产品经理：
我们的目标是构建一个的在线会议全生命管理系统。会议包含 3 个阶段：会前、会中以及会后。
每个的会议阶段都有我们可以解决的问题。在会议前，我们帮用户预约会议。
用户可以关联自己的日历，包括 Google 的日历，以及 Outlook 的日历。通过在系统上操作，用户可以预约一个会议。

系统分析师：
如何预约会议呢？

产品经理：
在系统界面上，用户打开属于他自己的日历，然后选择日期，选择时间段预约会议。
输入的内容有会议地址，如果是线上会议就输入会议的 URL。保存好会议之后，再把会议邀请发给其他与会者。

系统分析师：
如何发给与会者呢？

产品经理：
用户可以在界面上输入其他与会者的电子邮箱地址，这样系统通过电子邮件发会议邀请给与会者。

系统分析师：
请描述一下会议中，系统可以帮助用户哪些方面。

产品经理：
在会议中，系统帮助用户，做翻译，例如一个日本用户与美国用户在通过 Zoom 开会的时候，
针对美国用户，系统通过语音转文字的形式把日文翻译成英语；
针对日本用户，系统通过语音转文字的形式把英语翻译成日文。此外，会议的录音还保存在工作区中。

系统分析师：
什么是工作区？

产品经理：
每个用户在注册的时候都会分配一个默认的工作区，他可以邀请其他用户到他的工作区，
工作区保存着会议相关的一些资料，也包括着会议录音。工作区还包含着所有的会议信息。
加入 workspace 的概念之后，将 user 与 record/meeting 之间的直接关联打断，
每一个 user 可以以不同的 role 拥有多个 workspace，而所有的 resource（关联到最终的 record 或者 meeting）
都是归属于 workspace，通过不同的访问策略（access）来分配给不同的 member 进行操作。

系统分析师：
你说了 Member 这个概念，什么是 Member？

产品经理：
Member 是相对于工作区来说了，就是说一个工作区可以包含多个 Member，工作区的主人可以邀请其他用户进入他的工作区，工作区的主人可以为 Member 分配权限。
Member 通过权限来访问工作区的资源。
系统分析师：
一个用户可以创建多少个工作区？

产品经理：
这个没有限制，可以有无限多个工作区。

系统分析师：
工作区的拥有者可以邀请多少用户进入他的工作区。

产品经理：
用户需要为某个工作空间购买权益，我们的权益类似于手机套餐的通话时长、流量、附加功能这种，购买权益之后，
可以选择邀请有限数量的其他用户加入到自己的空间，归属于这个 workspace 的所有成员共享该 workspace 的权益。
权益目前分为时长和功能的开关，来源于购买商品或者赠送商品。

系统分析师：
会议结束后，系统可以帮助客户做什么呢？

产品经理：
会议后我们可以帮助做会议纪要，并发送给与会者。

系统分析师：
咱们希望支持的会议系统有哪些？
产品经理：
在线会议产品 A 和 B。你有想法能够帮助我实现这样的功能吗？

系统分析师：
当然，技术上我们可以为每个会议创建一个与会者，叫做会议助手，它其实是一个机器人（Bot）。
通过它，会议的语音就可以被系统实时接收到，通过翻译模块做翻译，翻译成文字，然后也可以把它记录下来。
'''
    }

    # Create and run the crew
    result = DddExpertCrew().crew().kickoff(inputs=inputs)

    # Print the result
    print("\n\n=== FINAL REPORT ===\n\n")
    print(result.raw)

    print("\n\nReport has been saved to output/domain_model.md")

if __name__ == "__main__":
    run()