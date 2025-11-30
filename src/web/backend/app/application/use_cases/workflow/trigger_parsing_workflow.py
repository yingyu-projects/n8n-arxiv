"""Trigger parsing workflow use case."""
from typing import List, Dict, Any
from app.domain.paper.repositories.paper_repository import PaperRepository
from app.domain.config.repositories.config_repository import ConfigRepository
from app.domain.paper.services.paper_domain_service import PaperDomainService
from app.domain.workflow.services.paper_parsing_service import PaperParsingService
from app.domain.paper.value_objects.summary import Summary
from app.infrastructure.external.arxiv_client import ArxivClient
from app.infrastructure.external.pdf_client import PdfClient
from app.infrastructure.external.llm_client import LLMClient, create_llm_client
from app.infrastructure.services.text_cleaner import TextCleaner
from app.infrastructure.services.config_loader import ConfigLoader
from app.infrastructure.services.workflow_status_manager import WorkflowStatusManager


class TriggerParsingWorkflowUseCase:
    """Use case for triggering the arXiv parsing workflow."""
    
    def __init__(
        self,
        paper_repository: PaperRepository,
        config_repository: ConfigRepository,
        arxiv_client: ArxivClient,
        pdf_client: PdfClient,
        text_cleaner: TextCleaner,
        config_loader: ConfigLoader,
        status_manager: WorkflowStatusManager,
    ):
        """Initialize use case."""
        self._paper_repository = paper_repository
        self._config_repository = config_repository
        self._arxiv_client = arxiv_client
        self._pdf_client = pdf_client
        self._text_cleaner = text_cleaner
        self._config_loader = config_loader
        self._status_manager = status_manager
        self._paper_domain_service = PaperDomainService(paper_repository)
        self._parsing_service = PaperParsingService()
    
    async def execute(
        self,
        categories: List[str],
        num_papers: int = 50,
    ) -> Dict[str, Any]:
        """Execute workflow."""
        try:
            # Estimate total papers (will be updated as we discover actual count)
            estimated_total = num_papers * len(categories)
            
            # Start workflow in status manager
            await self._status_manager.start_workflow(estimated_total)
            
            # Create LLM client
            llm_client = create_llm_client(self._config_loader)
            
            # Load prompt from database
            config = await self._config_repository.find_by_key('summarize_prompt')
            if config:
                summarize_prompt = config.value
            else:
                # Fallback to default prompt if not in database
                summarize_prompt = """你是一位顶尖的 AI 领域科学家兼科学传播者。请**精读以下清洗后的论文全文**，并完成一次深度归纳。目标不是复述，而是**帮助读者建立心智模型**——让他们理解：问题为何难？作者如何想到这个解法？它为何有效？边界在哪？  > 在我随后提供论文（PDF 或纯文本）后，请严格按照下面格式给出精要、准确、可引用的总结。**不要生成任何代码。**  ---  ## 输出格式（必须严格遵守） * JSON ###  JSON 字段: * topic: string, 论文题目（中英文）  * content:  string, 论文解析内容。 内容的具体格式定义如下：   ### 关键要点（要点化，6–10 条）  * 每条 12–20 字左右 * 覆盖：问题、方法、主要结果、影响   ### 三句话电梯陈述  * 面向科研/工程决策者，说明"这篇论文要解决什么问题 / 为什么重要 / 值不值得关注"  ### 技术概述（精炼）  #### 问题定义（1–2 段）  * 清晰界定研究问题与挑战  #### 提出的方法/模型/算法（1 段，强调新颖点）  * 简要描述方法核心与创新之处  #### 关键假设与理论基础（短列点）  * 列出重要假设与依赖的理论结果  ### 实验与结果（精确）  #### 用到的数据集、评价指标和基线（列出名称）  * 明确列出所有数据集、主要评价指标与对比基线  #### 主要结果  * 提供关键数值（例如准确率、误差、提升百分比等） * 标注这些数值来自论文的哪个表或图（例如"表2"或"图3"） * 若论文没有给出某些常见对比或置信区间，请指出缺失项  ### 优点与创新点（列点）  * 至少 3 点，写明为何比现有工作更好或不同  ### 局限性与风险（列点）  * 至少 3 点，包括：方法局限、实验局限、可重复性、推广性、伦理/社会风险（若相关）  ### 可复现性检查清单（短）  * 给出 6 个易检验项，例如：    1. 数据是否公开   2. 训练细节是否完整   3. 超参说明   4. 随机种子   5. 代码/模型权重是否公开   6. 所需计算资源  ### 后续工作建议（可操作，3–5 条）  * 包括改进实验、消融项、应用场景或理论扩展   ### 主题关键词（5–10 个）  * 便于索引和检索  ### 题目  * 原英文题目 * 中文翻译  ### 论文链接 * 论文链接  ### 作者  *作者信息（姓名 / 所属机构）  ### 未来应用场景 * 讨论未来此研究成果的应用场景和潜力  ### 最终结论与推荐（1 段）  * 明确建议（例如："值得深入阅读 / 可作为参考 / 仅作背景阅读 / 不推荐引用"） * 给出 1–2 条理由支持该建议  ---  ## 风格与长度要求  * 语言：中文（专业但简洁） * 避免长篇大论，把握要点 * 总长度控制在 **500–900 字**（最后不用显示列出解析字数） * **绝对不要生成或附带任何代码、伪代码或可执行命令**  ---  ## 额外注意事项  * 若论文包含数学证明或关键公式：**只用一句话概括其结论和用途**，不要逐步推导。 * 若论文引用了外部关键资源（公开数据集、预训练模型、重要工具）：请列出资源名称并说明是否公开可用。 * 若论文是综述/ survey：把"方法/实验"部分改为"覆盖主题与比较框架"，并提供对比表格（要点形式）。 * 若论文质量明显不好（例如实验设计严重缺陷或结果无法支撑结论）：在"局限性"中清楚标注，并在"最终结论"中给出明确负面建议。以下是论文正文："""
            
            # Process each category
            for category in categories:
                # Check if stop requested
                if await self._status_manager.should_stop():
                    await self._status_manager.mark_stopped()
                    break
                
                try:
                    # Fetch papers from arXiv
                    papers_data = self._arxiv_client.fetch_papers(category, num_papers)
                    
                    # Process each paper
                    for paper_data in papers_data:
                        # Check if stop requested
                        if await self._status_manager.should_stop():
                            await self._status_manager.mark_stopped()
                            break
                        
                        try:
                            pdf_link = paper_data["pdf_link"]
                            
                            # Check if paper already exists
                            exists = await self._paper_domain_service.ensure_paper_not_duplicate(pdf_link)
                            if not exists:
                                await self._status_manager.update_progress(skipped=1)
                                continue
                            
                            # Get or create paper
                            paper, is_new = await self._paper_domain_service.get_or_create_paper(
                                title=paper_data["title"],
                                pdf_link=pdf_link,
                                category=category,
                                arxiv_id=paper_data.get("arxiv_id"),
                            )
                            
                            # Validate paper for parsing
                            if not self._parsing_service.validate_paper_for_parsing(paper):
                                await self._status_manager.update_progress(skipped=1)
                                continue
                            
                            # Download and extract PDF
                            raw_text = self._pdf_client.download_and_extract(pdf_link)
                            
                            # Clean text
                            cleaned_text = self._text_cleaner.clean(raw_text)
                            prepared_text = self._parsing_service.prepare_paper_for_summary(
                                paper, cleaned_text
                            )
                            
                            # Generate summary using LLM
                            summary_dict = llm_client.summarize(
                                summarize_prompt,
                                prepared_text,
                                pdf_link
                            )
                            
                            # Create summary value object
                            summary = Summary.from_dict(summary_dict)
                            
                            # Mark paper as parsed
                            paper.mark_as_parsed(summary)
                            
                            # Save paper
                            await self._paper_repository.save(paper)
                            
                            paper_info = {
                                "id": str(paper.id),
                                "title": paper.title,
                                "pdf_link": pdf_link,
                            }
                            await self._status_manager.update_progress(
                                processed=1,
                                papers=[paper_info]
                            )
                            
                        except Exception as e:
                            error_msg = f"Error processing paper {paper_data.get('title', 'unknown')}: {str(e)}"
                            await self._status_manager.update_progress(errors=[error_msg])
                            continue
                            
                except Exception as e:
                    error_msg = f"Error processing category {category}: {str(e)}"
                    await self._status_manager.update_progress(errors=[error_msg])
                    continue
                
                # Check if stop requested after category
                if await self._status_manager.should_stop():
                    await self._status_manager.mark_stopped()
                    break
            
            # Mark workflow as completed
            await self._status_manager.complete_workflow()
            
        except Exception as e:
            await self._status_manager.mark_error(f"Workflow error: {str(e)}")
        
        # Return final status
        status = await self._status_manager.get_status()
        return {
            "processed": status["processed"],
            "skipped": status["skipped"],
            "errors": status["errors"],
            "papers": status["papers"],
        }

