import random
from http import HTTPStatus

from dashscope import Generation
class AI:
    def __init__(self):
        self.role="helpful assistant"
        self.limit_words=30
        self.__messages=[]
        self.mode=0
        #level表示ai回复偏客观还是主观,0表示主观,1表示客观
        self.level=1
        #tone表示ai回复的语气语调,1表示平静,2表示可爱俏皮,3表示活泼,4表示严肃,5表示开心,6表示伤感,7表示激动高涨
        self.tone=1

    def __init__(self,role,limit_words):
        self.role=role
        self.limit_words=limit_words
        self.__messages=[]
        self.mode=0
        self.level = 1
        self.tone=1

    def __init__(self,role,limit_words,mode,level,tone):
        self.role=role
        self.limit_words=limit_words
        self.__messages=[]
        self.mode=mode
        self.level = level
        self.tone=tone

    def __generate_prompt_template(self,message):
        msg = f"{message},回答字数限制在{self.limit_words}个字以内"
        if self.mode==1:
            msg+=",回答用户的问题之后再根据用户的回答对用户提一个相关的问题"
        elif self.mode==2:
            msg+=",回答用户的问题之后尽可能地让用户一些联想思考发散的空间"
        elif self.mode==3:
            msg+=",不直接回答用户的问题,但是给予用户一些提示让他自行思考"

        if self.level == 0:
            msg += ",内容可以带有一定的主观色彩,尽可能地发挥自己的联想"
        elif self.level == 1:
            msg += ",内容尽可能地客观中立"

        if self.tone==1:
            msg+=",语气尽量平静一点"
        elif self.tone==2:
            msg += ",语气尽量可爱俏皮一点,必要时可以适当撒娇卖萌"
        elif self.tone==3:
            msg+=",语气尽量活泼一点"
        elif self.tone==4:
            msg+=",语气尽量严肃一点"
        elif self.tone==5:
            msg+=",语气尽量表现得开心一些"
        elif self.tone==6:
            msg+=",语气情绪尽量表现得伤感一点,像是有心事的样子"
        elif self.tone==7:
            msg+=",情绪尽可能激烈高涨一点"
        return msg

    def chat(self,message):
        msg=self.__generate_prompt_template(message)
        #print(msg)
        self.__messages = [{'role': 'system', 'content': f'You are a {self.role}.'},
                    {'role': 'user', 'content': f"{msg},回答字数限制在{self.limit_words}个字以内"}]
        response = Generation.call(model="qwen-turbo",
                                   messages=self.__messages,
                                   # 设置随机数种子seed，如果没有设置，则随机数种子默认为1234
                                   seed=random.randint(1, 10000),
                                   temperature=0.8,
                                   top_p=0.8,
                                   top_k=50,
                                   # 将输出设置为"message"格式
                                   result_format='message')
        if response.status_code == HTTPStatus.OK:
            return response.output.choices[0].message.content
        return response.message

    def multipart_chat(self,message):
        msg = self.__generate_prompt_template(message)
        self.__messages.append({'role': 'system', 'content': f'You are a {self.role}.'})
        self.__messages.append({'role': 'user', 'content': f"{msg},回答字数限制在{self.limit_words}个字以内"})

        response = Generation.call(model="qwen-turbo",
                                   messages=self.__messages,
                                   # 设置随机数种子seed，如果没有设置，则随机数种子默认为1234
                                   seed=random.randint(1, 10000),
                                   temperature=0.8,
                                   top_p=0.8,
                                   top_k=50,
                                   # 将输出设置为"message"格式
                                   result_format='message')
        if response.status_code == HTTPStatus.OK:
            return response.output.choices[0].message.content
        return response.message

    def multipart_stream_chat(self,message):
        msg = self.__generate_prompt_template(message)
        self.__messages.append({'role': 'system', 'content': f'You are a {self.role}.'})
        self.__messages.append({'role': 'user', 'content': f"{msg},回答字数限制在{self.limit_words}个字以内"})

        responses = Generation.call(model="qwen-turbo",
                                   messages=self.__messages,
                                   # 设置随机数种子seed，如果没有设置，则随机数种子默认为1234
                                   seed=random.randint(1, 10000),
                                   temperature=0.8,
                                   top_p=0.8,
                                   top_k=50,
                                   stream=True,
                                   # 增量式流式输出
                                   incremental_output=True,
                                   # 将输出设置为"message"格式
                                   result_format='message')
        full_content = ""
        for response in responses:
            if response.status_code == HTTPStatus.OK:
                res = response.output.choices[0].message.content
                full_content += res
                print(res, end="")
            else:
                full_content = response.message
                break
        print()
        return full_content

    def stream_chat(self,message):
        msg = self.__generate_prompt_template(message)
        self.__messages = [{'role': 'system', 'content': f'You are a {self.role}.'},
                         {'role': 'user', 'content': f"{msg},回答字数限制在{self.limit_words}个字以内"}]
        responses = Generation.call(model="qwen-turbo",
                                   messages=self.__messages,
                                   # 设置随机数种子seed，如果没有设置，则随机数种子默认为1234
                                   seed=random.randint(1, 10000),
                                   temperature=0.8,
                                   top_p=0.8,
                                   top_k=50,
                                   stream=True,
                                   # 增量式流式输出
                                   incremental_output=True,
                                   # 将输出设置为"message"格式
                                   result_format='message')
        full_content=""
        for response in responses:
            if response.status_code == HTTPStatus.OK:
                res=response.output.choices[0].message.content
                full_content += res
                print(res,end="")
            else:
                full_content=response.message
                break
        print()
        return full_content