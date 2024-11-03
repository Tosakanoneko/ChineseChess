from openai import OpenAI
import time
import threading

def read_gpt(gpt):
    gpt.chat()

class CC_GPT:
	def __init__(self):
		self.client1 = OpenAI(
	    	api_key = "sk-56rYLjt47rroSg5vFw0omX1A82il0EIJRgTTb041XsUDaaZr", # 在这里将 MOONSHOT_API_KEY 替换为你从 Kimi 开放平台申请的 API Key
	    	base_url = "https://api.moonshot.cn/v1",
		)
		self.client2 = OpenAI(
	    	api_key = "sk-XZPStRqCRPteBsgcdUPtzOe0efaIIutuRtToIsRxlaLbgPj0", # 在这里将 MOONSHOT_API_KEY 替换为你从 Kimi 开放平台申请的 API Key
	    	base_url = "https://api.moonshot.cn/v1",
		)

		self.messages = [
			{"role": "system", "content": "你是一款名为智弈的象棋教育机器人上所搭载的象棋教育助手，能够对象棋的棋局进行详细的分析和解读，并给出不同的下法中最优的方案。当用户将他的走棋告诉你时，你能结合专业的象棋术语来给出合乎象棋规则的优质分析。你的回答需要言简意赅。"},
		]

		self.gpt_message = ''

		self.output_mark = False
		self.switch_mark = False
		self.SendToUI_mark = False

		self.usr_mv = ""
		self.best_mv = ""
		self.current_turn = ""
		self.chat_mark = False

	def chat(self):
		"""
		chat 函数支持多轮对话，每次调用 chat 函数与 Kimi 大模型对话时，Kimi 大模型都会”看到“此前已经
		产生的历史对话消息，换句话说，Kimi 大模型拥有了记忆。
		"""

		# 我们将用户最新的问题构造成一个 message（role=user），并添加到 messages 的尾部
		try:
			while True:
				if self.chat_mark:
					if self.current_turn == '红方':
						if self.usr_mv != self.best_mv:
							self.messages.append({
								"role": "user",
								"content": "用户（红方）走棋：" + self.usr_mv + "；最佳走棋：" + self.best_mv + "；对用户走棋进行分析，以及为什么最佳走棋的走法相比于用户的走法是更好的？用一段话回答，尽可能言简意赅。",
							})
							self.output_mark = True
						else:
							self.messages.append({
							"role": "user",
							"content": "用户（红方）走棋：" + self.usr_mv + "记住并理解目前的象棋局面。",
						})
					elif self.current_turn == '黑方':
						self.messages.append({
							"role": "user",
							"content": "机器人（黑方）走棋：" + self.usr_mv + "记住并理解目前的象棋局面。",
						})
					# 携带 messages 与 Kimi 大模型对话
					if self.output_mark:
						if self.switch_mark:
							completion = self.client1.chat.completions.create(
	    					    model="moonshot-v1-8k",
	    					    messages=self.messages,
	    					    temperature=0.3,
	    					)
							self.switch_mark = False
						else:
							completion = self.client2.chat.completions.create(
	    					    model="moonshot-v1-8k",
	    					    messages=self.messages,
	    					    temperature=0.3,
	    					)
							self.switch_mark = True

						assistant_message = completion.choices[0].message
						self.messages.append(assistant_message)
						if self.output_mark:
							self.gpt_message = assistant_message.content
							self.SendToUI_mark = True
							print(assistant_message.content)
							self.output_mark = False

					self.chat_mark = False
				time.sleep(1)
						# return assistant_message.content
		except KeyboardInterrupt:
			exit()
	def set_chat_msg(self, usr_mv, best_mv, turn):
		self.usr_mv = usr_mv
		self.best_mv = best_mv
		self.current_turn = turn
		self.chat_mark = True

if __name__ == '__main__':
	gpt = CC_GPT()
	chat_thread = threading.Thread(target=gpt.chat)
	chat_thread.setDaemon(True)
	chat_thread.start()
	gpt.set_chat_msg("车一进一", "兵三进一", "红方")
	chat_thread.join()