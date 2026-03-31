import json
import base64
from typing import Optional, List, Dict
from openai import OpenAI
from app.core.config import settings
from app.core.exceptions import BusinessException

class VolcengineAIService:
    """火山引擎大模型服务封装，使用OpenAI SDK调用"""

    def __init__(self):
        self.api_key = settings.VOLCENGINE_API_KEY
        self.model = settings.VOLCENGINE_MODEL
        self.client = OpenAI(
            base_url="https://ark.cn-beijing.volces.com/api/v3",
            api_key=self.api_key,
        )

    async def _chat_completion(self, messages: List[Dict], temperature: float = 0.7) -> str:
        """通用调用大模型接口"""
        print("="*50)
        print("开始调用火山引擎大模型")
        print(f"模型: {self.model}")
        print(f"请求消息数: {len(messages)}")
        print(f"API密钥已配置: {'是' if self.api_key else '否'}")

        if not self.api_key:
            print("错误：API密钥未配置")
            raise BusinessException(code=500001, message="火山引擎API密钥未配置")

        try:
            print("正在发送请求...")
            response = self.client.responses.create(
                model=self.model,
                input=messages,
                temperature=temperature,
                stream=False,
                timeout=120.0,  # 超时时间设置为2分钟
                extra_body={
                    "thinking": {"type": "disabled"}  # 禁用深度思考，加快返回速度
                }
            )
            print(f"请求成功，响应ID: {response.id}")
            print(f"输出内容预览: {response.output_text[:300]}...")
            print("="*50)
            return response.output_text
        except Exception as e:
            print(f"调用大模型失败，错误类型: {type(e).__name__}")
            print(f"错误详情: {str(e)}")
            import traceback
            traceback.print_exc()
            print("="*50)
            raise BusinessException(code=500002, message=f"调用大模型失败: {str(e)}")

    async def resume_parse(self, text_content: str = None, images: List[str] = None) -> Dict:
        """简历解析，支持文本内容或图片（base64）列表，返回结构化JSON"""
        content = []
        if images:
            # 多模态模式，传入图片
            print(f"[大模型调用] 传入{len(images)}张图片进行解析")
            for img_base64 in images:
                content.append({
                    "type": "input_image",
                    "image_url": f"data:image/png;base64,{img_base64}"
                })
        elif text_content:
            # 文本模式
            print(f"[大模型调用] 传入文本内容，长度：{len(text_content)}字符")
            content.append({
                "type": "input_text",
                "text": f"简历内容：\n{text_content}"
            })

        prompt = """
        请解析以下简历内容，返回结构化JSON数据，严格包含以下字段，不要多余字段：
        - personal_info: 个人信息对象，包含姓名、电话、邮箱、年龄、性别、所在城市，字段不存在时为null
        - education: 教育经历数组，每个对象包含school_name(学校名称)、major(专业)、education(学历)、start_date(开始时间，YYYY-MM或YYYY-MM-DD格式，至今为null)、end_date(结束时间，同上)、description(描述)，字段不存在时为null
        - work_experience: 工作经历数组，每个对象包含company_name(公司名称)、position(职位)、start_date(开始时间)、end_date(结束时间)、description(工作描述)、achievements(工作业绩)，字段不存在时为null
        - project_experience: 项目经历数组，每个对象包含project_name(项目名称)、role(角色)、start_date(开始时间)、end_date(结束时间)、description(项目描述)、achievements(项目成果)，字段不存在时为null
        - skills: 字符串数组，技能标签列表，没有则为空数组
        - self_introduction: 字符串，自我介绍内容，没有则为null

        严格只返回标准JSON格式，不要任何其他解释文字、markdown标记、反引号等，确保可以直接用JSON.parse解析。所有日期请统一格式为YYYY-MM或者YYYY-MM-DD。
        """
        content.append({
            "type": "input_text",
            "text": prompt
        })

        messages = [{"role": "user", "content": content}]
        result = await self._chat_completion(messages)

        # 清理可能的markdown标记和多余内容
        result = result.strip()
        if result.startswith("```json"):
            result = result[7:]
        if result.endswith("```"):
            result = result[:-3]
        # 提取第一个完整的JSON对象
        import re
        import json
        from app.core.exceptions import BusinessException

        # 先检查是否为空
        if not result or len(result) < 10:
            raise BusinessException(code=500003, message="简历解析返回内容为空")

        print(f"[DEBUG] 原始返回内容: {result[:800]}...")

        # 先尝试直接解析原始内容
        try:
            parsed = json.loads(result)
            print(f"[DEBUG] 直接解析成功")
        except Exception as e:
            print(f"[DEBUG] 直接解析失败: {e}，尝试修复")
            # 提取JSON部分
            json_match = re.search(r'\{[\s\S]*\}', result)
            if json_match:
                result = json_match.group(0)
                print(f"[DEBUG] 提取JSON部分: {result[:800]}...")
            result = result.strip()

            # 处理截断情况：如果检测到内容不完整，尝试补全到至少能解析基础结构
            def fix_json(json_str):
                # 第一步：基础清理
                json_str = re.sub(r'[\x00-\x1F\x7F]', '', json_str)  # 移除控制字符
                json_str = json_str.replace('　', ' ')  # 全角空格转半角
                json_str = json_str.replace('\n', ' ').replace('\r', ' ')  # 移除换行
                json_str = re.sub(r'\s+', ' ', json_str)  # 合并多个空格

                # 第二步：处理常见格式错误
                json_str = json_str.replace("'", '"')  # 单引号转双引号
                json_str = re.sub(r'(\w+)(?=\s*:)', r'"\1"', json_str)  # 给未加引号的键加引号
                json_str = re.sub(r',\s*([}\]])', r'\1', json_str)  # 移除尾随逗号
                json_str = json_str.replace('None', 'null').replace('none', 'null')
                json_str = json_str.replace('True', 'true').replace('False', 'false')

                # 第三步：自动补全括号（处理截断）
                stack = []
                in_string = False
                escape = False
                for char in json_str:
                    if escape:
                        escape = False
                        continue
                    if char == '\\':
                        escape = True
                        continue
                    if char == '"':
                        in_string = not in_string
                        continue
                    if not in_string:
                        if char == '{' or char == '[':
                            stack.append(char)
                        elif char == '}' and stack and stack[-1] == '{':
                            stack.pop()
                        elif char == ']' and stack and stack[-1] == '[':
                            stack.pop()

                # 补全未闭合的括号
                while stack:
                    last = stack.pop()
                    if last == '{':
                        json_str += '}'
                    elif last == '[':
                        json_str += ']'

                return json_str

            # 尝试修复后解析
            fixed_result = fix_json(result)
            print(f"[DEBUG] 修复后内容: {fixed_result[:800]}...")

            # 尝试多种解析方式
            parsers = [
                lambda s: json.loads(s),
                lambda s: __import__('json5').loads(s),
                lambda s: __import__('ast').literal_eval(s)
            ]

            parsed = None
            for parser in parsers:
                try:
                    parsed = parser(fixed_result)
                    print(f"[DEBUG] 使用{parser.__name__}解析成功")
                    break
                except Exception as e2:
                    print(f"[DEBUG] {parser.__name__}解析失败: {e2}")
                    continue

            # 所有解析都失败，尝试分段提取可用字段
            if not parsed:
                print(f"[DEBUG] 尝试分段提取字段")
                parsed = {
                    "personal_info": {"姓名": "", "电话": "", "邮箱": "", "所在城市": ""},
                    "education": [],
                    "work_experience": [],
                    "project_experience": [],
                    "skills": [],
                    "self_introduction": ""
                }

                # 尝试提取个人信息
                try:
                    pi_match = re.search(r'"personal_info"\s*:\s*(\{.*?\})(?=\s*,\s*"|\s*\})', result, re.DOTALL)
                    if pi_match:
                        pi_str = pi_match.group(1)
                        # 修复个人信息部分的JSON
                        pi_str = re.sub(r',\s*([}\]])', r'\1', pi_str)
                        personal_info = json.loads(pi_str)
                        if isinstance(personal_info, dict):
                            parsed["personal_info"] = personal_info
                            print(f"[DEBUG] 分段提取个人信息成功: {personal_info}")
                except Exception as e:
                    print(f"[DEBUG] 提取个人信息失败: {e}")

                # 尝试提取教育经历
                try:
                    edu_match = re.search(r'"education"\s*:\s*(\[.*?\])(?=\s*,\s*"|\s*\})', result, re.DOTALL)
                    if edu_match:
                        edu_str = edu_match.group(1)
                        # 修复多余的括号
                        edu_str = edu_str.rstrip('])}') + ']'
                        edu_str = re.sub(r',\s*([}\]])', r'\1', edu_str)
                        education = json.loads(edu_str)
                        if isinstance(education, list):
                            parsed["education"] = education
                            print(f"[DEBUG] 分段提取教育经历成功: {len(education)}条")
                except Exception as e:
                    print(f"[DEBUG] 提取教育经历失败: {e}")

                # 尝试提取工作经历
                try:
                    work_match = re.search(r'"work_experience"\s*:\s*(\[.*?\])(?=\s*,\s*"|\s*\})', result, re.DOTALL)
                    if work_match:
                        work_str = work_match.group(1)
                        work_str = work_str.rstrip('])}') + ']'
                        work_str = re.sub(r',\s*([}\]])', r'\1', work_str)
                        work_experience = json.loads(work_str)
                        if isinstance(work_experience, list):
                            parsed["work_experience"] = work_experience
                            print(f"[DEBUG] 分段提取工作经历成功: {len(work_experience)}条")
                except Exception as e:
                    print(f"[DEBUG] 提取工作经历失败: {e}")

                # 尝试提取项目经历
                try:
                    proj_match = re.search(r'"project_experience"\s*:\s*(\[.*?\])(?=\s*,\s*"|\s*\})', result, re.DOTALL)
                    if proj_match:
                        proj_str = proj_match.group(1)
                        proj_str = proj_str.rstrip('])}') + ']'
                        proj_str = re.sub(r',\s*([}\]])', r'\1', proj_str)
                        project_experience = json.loads(proj_str)
                        if isinstance(project_experience, list):
                            parsed["project_experience"] = project_experience
                            print(f"[DEBUG] 分段提取项目经历成功: {len(project_experience)}条")
                except Exception as e:
                    print(f"[DEBUG] 提取项目经历失败: {e}")

                # 尝试提取技能
                try:
                    skills_match = re.search(r'"skills"\s*:\s*(\[.*?\])(?=\s*,\s*"|\s*\})', result, re.DOTALL)
                    if skills_match:
                        skills_str = skills_match.group(1)
                        skills_str = skills_str.rstrip('])}') + ']'
                        skills = json.loads(skills_str)
                        if isinstance(skills, list):
                            parsed["skills"] = skills
                            print(f"[DEBUG] 分段提取技能成功: {len(skills)}个")
                except Exception as e:
                    print(f"[DEBUG] 提取技能失败: {e}")

                # 尝试提取自我介绍
                try:
                    intro_match = re.search(r'"self_introduction"\s*:\s*"([^"]*?)"', result, re.DOTALL)
                    if intro_match:
                        parsed["self_introduction"] = intro_match.group(1)
                        print(f"[DEBUG] 分段提取自我介绍成功")
                except Exception as e:
                    print(f"[DEBUG] 提取自我介绍失败: {e}")

        # 校验基础字段是否存在，补全缺失字段
        required_fields = ["personal_info", "education", "work_experience", "project_experience", "skills", "self_introduction"]
        for field in required_fields:
            if field not in parsed:
                parsed[field] = [] if field.endswith('s') else {}

        if not isinstance(parsed["personal_info"], dict):
            parsed["personal_info"] = {}
        for list_field in ["education", "work_experience", "project_experience", "skills"]:
            if not isinstance(parsed[list_field], list):
                parsed[list_field] = []

        print(f"[DEBUG] 最终解析结果: {parsed}")
        return parsed

    async def resume_evaluate(self, resume_content: Dict) -> Dict:
        """简历评测，给出评分和优化建议"""
        prompt = f"""
        请对以下简历进行评测，返回JSON格式结果：
        - score: 0-100分的综合评分
        - evaluation: 整体评价文字
        - advantages: 优点列表
        - disadvantages: 不足列表
        - suggestions: 具体优化建议列表

        只返回JSON，不要其他解释内容。

        简历内容：
        {json.dumps(resume_content, ensure_ascii=False)}
        """

        messages = [{"role": "user", "content": prompt}]
        result = await self._chat_completion(messages)
        try:
            return json.loads(result)
        except json.JSONDecodeError:
            raise BusinessException(code=500004, message="简历评测结果格式错误")

    async def job_match(self, resume_content: Dict, job_content: Dict) -> Dict:
        """人岗匹配分析"""
        prompt = f"""
        请分析以下简历和岗位的匹配度，返回JSON格式结果：
        - match_score: 0-100分的匹配度评分
        - match_analysis: 整体匹配分析文字
        - advantages: 匹配优势列表
        - disadvantages: 差距列表
        - suggestions: 改进建议列表

        只返回JSON，不要其他解释内容。

        简历内容：
        {json.dumps(resume_content, ensure_ascii=False)}

        岗位内容：
        {json.dumps(job_content, ensure_ascii=False)}
        """

        messages = [{"role": "user", "content": prompt}]
        result = await self._chat_completion(messages)
        try:
            return json.loads(result)
        except json.JSONDecodeError:
            raise BusinessException(code=500005, message="匹配分析结果格式错误")

    async def generate_interview_questions(self, resume_content: Dict, job_content: Dict) -> List[Dict]:
        """生成面试题"""
        prompt = f"""
        请根据以下简历和岗位信息，生成5-8道面试题，返回JSON数组，每个问题包含：
        - question: 问题内容
        - examination_point: 考察点
        - reference_answer: 参考答案

        只返回JSON数组，不要其他解释内容。

        简历内容：
        {json.dumps(resume_content, ensure_ascii=False)}

        岗位内容：
        {json.dumps(job_content, ensure_ascii=False)}
        """

        messages = [{"role": "user", "content": prompt}]
        result = await self._chat_completion(messages)
        try:
            return json.loads(result)
        except json.JSONDecodeError:
            raise BusinessException(code=500006, message="面试题生成结果格式错误")

    async def generate_interview_preparation(self, job_content: Dict) -> Dict:
        """生成面试准备：10个面试问题、参考答案和知识点梳理"""
        prompt = f"""
        请根据以下岗位信息，生成面试准备内容，返回JSON对象，包含：
        - interview_questions: 10个面试问题数组，每个问题包含：
            * question: 问题内容
            * reference_answer: 参考答案
            * key_points: 知识点梳理（数组）

        只返回JSON对象，不要其他解释内容。

        岗位内容：
        {json.dumps(job_content, ensure_ascii=False)}
        """

        messages = [{"role": "user", "content": prompt}]
        result = await self._chat_completion(messages, temperature=0.7)
        try:
            return json.loads(result)
        except json.JSONDecodeError:
            raise BusinessException(code=500007, message="面试准备生成结果格式错误")

# 单例实例
volcengine_ai_service = VolcengineAIService()
