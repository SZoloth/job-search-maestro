#!/usr/bin/env python3
"""
Interview Preparation Automation System

AI-powered interview preparation system that generates company-specific materials,
predicts interview questions, and creates structured STAR method responses based
on Sam's case story repository and research findings.

This system automates the interview preparation process by:
1. Generating company-specific question banks with AI
2. Creating interviewer research profiles and question predictions
3. Building STAR method response frameworks from case stories
4. Developing company-specific talking points and examples
5. Creating mock interview scenarios and practice guides

Success Outcomes:
- Interviewers consistently note superior business understanding
- More thoughtful questions than typical candidates
- Higher conversion rates from first round to offer
- Better preparation than internal employees

Usage:
    from interview_prep_system import InterviewPrepSystem
    
    prep_system = InterviewPrepSystem()
    materials = prep_system.generate_interview_prep("Canva", "Senior Product Manager")
"""

import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class InterviewPrepSystem:
    """
    Comprehensive interview preparation automation system.
    
    Implements Sam's AI-powered interview prep methodology:
    - Company-specific question prediction using AI research
    - Interviewer background research and question forecasting
    - STAR method response generation from case story repository
    - Company-specific talking points and value propositions
    - Mock interview scenarios and practice frameworks
    
    Integration Points:
    - Company research data from AI Research Engine
    - Case stories from repository for STAR responses
    - Job analysis from Application Generator
    - Role-specific competency frameworks
    """
    
    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.output_dir = Path("Applications")
        self.case_stories_path = Path("experience/Case_Stories_Repository.md")
        
        # Load interview preparation frameworks
        self.question_categories = self._load_question_categories()
        self.star_framework = self._load_star_framework()
        self.competency_models = self._load_competency_models()
        
        # AI prompts for interview preparation
        self.ai_prompts = self._load_interview_ai_prompts()
    
    def generate_interview_prep(self, company_name: str, role_title: str,
                              research_data: Dict = None, 
                              interviewer_list: List[Dict] = None) -> Dict:
        """
        Generate comprehensive interview preparation materials.
        
        Creates complete interview prep package:
        1. Company-specific question banks
        2. Interviewer research and question predictions  
        3. STAR method response frameworks
        4. Company-specific talking points
        5. Mock interview scenarios
        6. Questions to ask interviewers
        """
        logger.info(f"Generating interview prep materials for {company_name} - {role_title}")
        
        # Generate company-specific question bank
        logger.info("Creating company-specific question bank...")
        question_bank = self._generate_question_bank(company_name, role_title, research_data)
        
        # Research interviewers and predict their questions
        logger.info("Analyzing interviewers and predicting questions...")
        interviewer_analysis = self._analyze_interviewers(interviewer_list, company_name, role_title)
        
        # Generate STAR method responses
        logger.info("Creating STAR method response frameworks...")
        star_responses = self._generate_star_responses(role_title, question_bank, research_data)
        
        # Create company-specific talking points
        logger.info("Developing company-specific talking points...")
        talking_points = self._generate_talking_points(company_name, role_title, research_data)
        
        # Generate questions to ask interviewers
        logger.info("Creating interviewer questions...")
        interviewer_questions = self._generate_interviewer_questions(company_name, role_title, research_data)
        
        # Create mock interview scenarios
        logger.info("Building mock interview scenarios...")
        mock_scenarios = self._create_mock_scenarios(company_name, role_title, question_bank)
        
        # Compile comprehensive prep package
        prep_package = {
            "company_name": company_name,
            "role_title": role_title,
            "prep_date": datetime.now().isoformat(),
            "question_bank": question_bank,
            "interviewer_analysis": interviewer_analysis,
            "star_responses": star_responses,
            "talking_points": talking_points,
            "interviewer_questions": interviewer_questions,
            "mock_scenarios": mock_scenarios,
            "ai_prep_prompts": self._generate_ai_prep_prompts(company_name, role_title),
            "preparation_checklist": self._generate_prep_checklist()
        }
        
        # Save prep materials to company folder
        self._save_interview_prep(prep_package)
        
        logger.info(f"Interview prep materials generated for {company_name}")
        return prep_package
    
    def _load_question_categories(self) -> Dict[str, List[str]]:
        """Load interview question categories and templates."""
        return {
            "behavioral": [
                "Tell me about a time when you had to make a difficult decision with limited information",
                "Describe a situation where you had to influence someone without direct authority",
                "Give me an example of when you had to pivot a project based on new information",
                "Tell me about a time when you disagreed with a stakeholder and how you handled it",
                "Describe a project that didn't go as planned and how you adapted"
            ],
            "product_strategy": [
                "How would you prioritize features for our product roadmap?",
                "Walk me through how you would approach entering a new market",
                "How do you balance technical debt vs. new feature development?",
                "Describe your framework for making build vs. buy decisions",
                "How would you approach improving our key metrics?"
            ],
            "growth_focused": [
                "How would you approach growing our user base by 50% in the next year?",
                "What metrics would you focus on to improve our conversion funnel?",
                "How do you balance acquisition vs. retention initiatives?",
                "Describe your approach to A/B testing and experimentation",
                "How would you identify and prioritize growth opportunities?"
            ],
            "technical_execution": [
                "How do you work with engineering teams to scope and deliver projects?",
                "Describe your experience with data analysis and SQL",
                "How do you ensure product requirements are clearly communicated?",
                "Tell me about your approach to user research and testing",
                "How do you stay informed about technical constraints and possibilities?"
            ],
            "leadership": [
                "Describe your experience mentoring or managing other PMs",
                "How do you handle conflicting priorities between different stakeholders?",
                "Tell me about a time when you had to deliver difficult feedback",
                "How do you build consensus when teams disagree on direction?",
                "Describe your approach to building and scaling product teams"
            ],
            "company_specific": [
                "Why do you want to work at [company]?",
                "What do you think are our biggest competitive advantages?",
                "How would you improve our current product?",
                "What challenges do you see in our industry?",
                "Where do you see our company in 3 years?"
            ]
        }
    
    def _load_star_framework(self) -> Dict:
        """Load STAR method framework for structured responses."""
        return {
            "definition": {
                "Situation": "Context and background - where, when, what was happening",
                "Task": "Your responsibility - what you needed to accomplish", 
                "Action": "What you did - your specific steps and decisions",
                "Result": "What happened - outcomes and impact achieved"
            },
            "best_practices": [
                "Be specific with metrics and quantifiable outcomes",
                "Focus on YOUR actions and contributions, not team achievements",
                "Choose examples that demonstrate relevant competencies",
                "Practice timing - aim for 2-3 minutes per response",
                "Connect results back to business impact when possible"
            ],
            "response_structure": {
                "opening": "Brief context setting (30 seconds)",
                "situation_task": "Clear problem definition (45 seconds)",
                "action": "Detailed action description (60-90 seconds)",
                "result": "Quantified outcomes and learnings (30-45 seconds)"
            }
        }
    
    def _load_competency_models(self) -> Dict[str, List[str]]:
        """Load competency models by role level and type."""
        return {
            "senior_product_manager": [
                "Strategic Thinking", "User Empathy", "Data-Driven Decision Making",
                "Cross-Functional Leadership", "Technical Acumen", "Communication",
                "Problem Solving", "Stakeholder Management", "Execution Excellence"
            ],
            "growth_product_manager": [
                "Growth Strategy", "Experimentation", "Funnel Optimization", 
                "User Acquisition", "Retention Strategy", "Analytics", 
                "A/B Testing", "Conversion Optimization", "Scalable Systems"
            ],
            "principal_product_manager": [
                "Vision Setting", "Strategic Planning", "Technical Leadership",
                "Organizational Influence", "Mentoring", "Complex Problem Solving",
                "Cross-Team Collaboration", "Business Acumen", "Innovation"
            ]
        }
    
    def _load_interview_ai_prompts(self) -> Dict[str, str]:
        """Load AI prompts for interview preparation automation."""
        return {
            "interviewer_research": """Research {interviewer_name} at {company_name}. Based on their background, role, and recent work, what types of questions would they likely ask a {role_title} candidate? What aspects of the business would they care most about? 

Consider:
- Their professional background and expertise areas
- Their role and responsibilities at the company  
- Recent projects or initiatives they've been involved in
- The skills and experience they would value most
- Potential areas of concern or focus for their team

Provide 8-10 specific, likely interview questions they might ask.""",
            
            "company_question_bank": """Based on the company dossier and role requirements, generate 15-20 likely interview questions for this {role_title} position at {company_name}. Include both behavioral and technical questions specific to their business challenges.

Company Context:
{company_context}

Role Focus Areas:
{role_focus_areas}

Include questions that cover:
- Company-specific challenges and opportunities
- Role-specific technical and strategic competencies
- Behavioral questions relevant to their culture and values
- Situational questions based on their current business priorities""",
            
            "star_response_coach": """For each question, help me structure a compelling response using the STAR method that highlights my relevant experience and quantified outcomes. Focus on stories that demonstrate {key_skills_for_role}.

Question: {interview_question}

Available Experience Examples:
{case_stories_summary}

Provide:
1. Recommended case story/experience to use
2. STAR structure outline with specific talking points
3. Key metrics and outcomes to emphasize  
4. Connection to the role requirements and company needs""",
            
            "company_talking_points": """Based on the company research, create key talking points that demonstrate deep understanding of {company_name}'s business, challenges, and opportunities. These should be conversation starters and demonstrate strategic thinking.

Include:
- 3-4 strategic insights about their market position
- 2-3 specific growth opportunities you've identified
- Key challenges they likely face and how you could help address them
- Questions that show you understand their business model
- Competitive dynamics and differentiation opportunities"""
        }
    
    def _generate_question_bank(self, company_name: str, role_title: str, 
                              research_data: Dict = None) -> Dict:
        """Generate comprehensive question bank for interview preparation."""
        # Get base questions by category
        base_questions = self.question_categories.copy()
        
        # Customize company-specific questions
        if research_data:
            company_questions = self._generate_company_specific_questions(
                company_name, role_title, research_data
            )
            base_questions["company_specific"] = company_questions
        
        # Add role-specific emphasis
        role_questions = self._get_role_specific_questions(role_title, base_questions)
        
        # Generate AI-powered question predictions
        ai_questions = self._generate_ai_question_predictions(
            company_name, role_title, research_data
        )
        
        question_bank = {
            "by_category": base_questions,
            "role_specific": role_questions,
            "ai_predictions": ai_questions,
            "high_probability": self._identify_high_probability_questions(
                base_questions, role_title
            ),
            "preparation_priority": self._prioritize_questions(
                base_questions, role_title, research_data
            )
        }
        
        return question_bank
    
    def _generate_company_specific_questions(self, company_name: str, role_title: str,
                                           research_data: Dict) -> List[str]:
        """Generate questions specific to the company and role."""
        questions = [
            f"Why do you want to work at {company_name}?",
            f"What do you think are {company_name}'s biggest competitive advantages?",
            f"How would you improve {company_name}'s current product?"
        ]
        
        # Add questions based on research findings
        if research_data:
            if "key_challenges" in research_data:
                questions.append(f"How would you approach {research_data['key_challenges']}?")
            
            if "recent_news" in research_data:
                questions.append(f"What do you think about {company_name}'s recent {research_data['recent_news']}?")
            
            if "competitive_landscape" in research_data:
                questions.append(f"How do you see {company_name} differentiating from competitors like [specific competitor]?")
        
        return questions
    
    def _get_role_specific_questions(self, role_title: str, base_questions: Dict) -> List[str]:
        """Get questions most relevant to the specific role."""
        role_lower = role_title.lower()
        
        relevant_questions = []
        
        if "growth" in role_lower:
            relevant_questions.extend(base_questions["growth_focused"][:5])
            relevant_questions.extend(base_questions["technical_execution"][:3])
        elif "senior" in role_lower or "principal" in role_lower:
            relevant_questions.extend(base_questions["product_strategy"][:5])
            relevant_questions.extend(base_questions["leadership"][:3])
        elif "strategy" in role_lower:
            relevant_questions.extend(base_questions["product_strategy"][:5])
            relevant_questions.extend(base_questions["behavioral"][:3])
        else:
            relevant_questions.extend(base_questions["product_strategy"][:3])
            relevant_questions.extend(base_questions["technical_execution"][:3])
        
        # Always include core behavioral questions
        relevant_questions.extend(base_questions["behavioral"][:3])
        
        return relevant_questions[:15]  # Limit to most relevant
    
    def _generate_ai_question_predictions(self, company_name: str, role_title: str,
                                        research_data: Dict = None) -> Dict:
        """Generate AI-powered question predictions."""
        # This would use AI prompts to predict likely questions
        ai_predictions = {
            "prompt_for_execution": self.ai_prompts["company_question_bank"].format(
                role_title=role_title,
                company_name=company_name,
                company_context=self._format_company_context(research_data),
                role_focus_areas=self._get_role_focus_areas(role_title)
            ),
            "execution_instructions": [
                "Execute the AI prompt above to generate company-specific questions",
                "Review and validate questions for relevance and likelihood",
                "Add questions to high-priority preparation list",
                "Use questions to guide STAR response preparation"
            ],
            "predicted_themes": self._predict_question_themes(company_name, role_title, research_data)
        }
        
        return ai_predictions
    
    def _format_company_context(self, research_data: Dict = None) -> str:
        """Format company context for AI prompt."""
        if not research_data:
            return "Company research data not available - use general industry context"
        
        context_elements = []
        
        if "business_model" in research_data:
            context_elements.append(f"Business Model: {research_data['business_model']}")
        
        if "key_challenges" in research_data:
            context_elements.append(f"Key Challenges: {research_data['key_challenges']}")
        
        if "competitive_landscape" in research_data:
            context_elements.append(f"Competitive Position: {research_data['competitive_landscape']}")
        
        if "recent_news" in research_data:
            context_elements.append(f"Recent Developments: {research_data['recent_news']}")
        
        return "\n".join(context_elements) if context_elements else "General company context"
    
    def _get_role_focus_areas(self, role_title: str) -> str:
        """Get focus areas for the role."""
        role_lower = role_title.lower()
        
        if "growth" in role_lower:
            return "User acquisition, conversion optimization, retention, experimentation, funnel analysis"
        elif "senior" in role_lower:
            return "Strategic planning, cross-functional leadership, stakeholder management, execution"
        elif "principal" in role_lower:
            return "Vision setting, technical strategy, organizational influence, complex problem solving"
        else:
            return "Product strategy, user research, roadmap planning, feature prioritization"
    
    def _predict_question_themes(self, company_name: str, role_title: str, 
                               research_data: Dict = None) -> List[str]:
        """Predict likely question themes based on company and role."""
        themes = [
            "Product strategy and roadmap prioritization",
            "Cross-functional collaboration and stakeholder management",
            "Data-driven decision making and experimentation"
        ]
        
        # Add company-specific themes
        if research_data:
            if "ai_initiatives" in research_data:
                themes.append("AI implementation and product integration")
            
            if "growth_challenges" in research_data:
                themes.append("Scaling challenges and growth strategy")
        
        # Add role-specific themes
        role_lower = role_title.lower()
        if "growth" in role_lower:
            themes.extend([
                "User acquisition and conversion optimization",
                "A/B testing and experimentation frameworks"
            ])
        elif "senior" in role_lower:
            themes.extend([
                "Leadership and team development",
                "Strategic vision and execution"
            ])
        
        return themes
    
    def _identify_high_probability_questions(self, questions: Dict, role_title: str) -> List[str]:
        """Identify questions with highest probability of being asked."""
        high_probability = [
            "Tell me about yourself / Walk me through your background",
            "Why do you want to work here?",
            "Why are you interested in this role?",
            "What's your experience with [key skill for role]?",
            "Tell me about a challenging project you led"
        ]
        
        # Add role-specific high-probability questions
        if "growth" in role_title.lower():
            high_probability.extend([
                "How do you approach growth experimentation?",
                "Tell me about a time you improved conversion rates"
            ])
        
        return high_probability
    
    def _prioritize_questions(self, questions: Dict, role_title: str,
                            research_data: Dict = None) -> Dict[str, List[str]]:
        """Prioritize questions by preparation importance."""
        return {
            "must_prepare": [
                "Tell me about yourself",
                f"Why do you want to work at [company]?",
                "Walk me through a challenging project",
                "How do you prioritize features/initiatives?",
                "Tell me about a time you had to influence without authority"
            ],
            "should_prepare": [
                "How do you approach [key skill]?",
                "Describe your experience with [relevant experience]",
                "How do you handle competing stakeholder priorities?",
                "Tell me about a failed project and what you learned",
                "How do you stay informed about industry trends?"
            ],
            "nice_to_prepare": [
                "Where do you see yourself in 5 years?",
                "What's your biggest weakness?",
                "Tell me about a time you disagreed with your manager",
                "How do you handle stress and pressure?",
                "What questions do you have for me?"
            ]
        }
    
    def _analyze_interviewers(self, interviewer_list: List[Dict] = None,
                            company_name: str = "", role_title: str = "") -> Dict:
        """Analyze interviewers and predict their likely questions."""
        if not interviewer_list:
            # Generate template interviewer profiles
            interviewer_list = self._generate_typical_interviewer_profiles(role_title)
        
        interviewer_analysis = {
            "profiles": [],
            "ai_research_prompts": [],
            "question_predictions": {},
            "preparation_strategy": {}
        }
        
        for interviewer in interviewer_list:
            # Generate AI research prompt for this interviewer
            research_prompt = self.ai_prompts["interviewer_research"].format(
                interviewer_name=interviewer.get("name", "Interviewer"),
                company_name=company_name,
                role_title=role_title
            )
            
            # Create interviewer profile
            profile = {
                "name": interviewer.get("name", "Unknown"),
                "title": interviewer.get("title", "Unknown"),
                "background": interviewer.get("background", "Research needed"),
                "likely_focus_areas": self._predict_interviewer_focus(interviewer),
                "preparation_notes": self._generate_interviewer_prep_notes(interviewer),
                "ai_research_prompt": research_prompt
            }
            
            interviewer_analysis["profiles"].append(profile)
            interviewer_analysis["ai_research_prompts"].append(research_prompt)
        
        return interviewer_analysis
    
    def _generate_typical_interviewer_profiles(self, role_title: str) -> List[Dict]:
        """Generate typical interviewer profiles for the role."""
        profiles = [
            {
                "name": "Hiring Manager",
                "title": "Head of Product / VP Product",
                "background": "Direct manager for the role",
                "focus_areas": ["Role fit", "Technical competence", "Team collaboration"]
            },
            {
                "name": "Peer PM",
                "title": "Senior Product Manager",
                "background": "Current team member",
                "focus_areas": ["Technical depth", "Collaboration style", "Problem-solving"]
            },
            {
                "name": "Engineering Lead",
                "title": "Engineering Manager / Tech Lead",
                "background": "Key collaboration partner", 
                "focus_areas": ["Technical understanding", "Requirement clarity", "Execution"]
            },
            {
                "name": "Design Partner",
                "title": "Senior Designer / Design Lead",
                "background": "Cross-functional partner",
                "focus_areas": ["User empathy", "Design collaboration", "User research"]
            },
            {
                "name": "Executive",
                "title": "CEO / CPO / VP",
                "background": "Senior leadership",
                "focus_areas": ["Strategic thinking", "Vision alignment", "Leadership potential"]
            }
        ]
        
        return profiles[:4]  # Return most common interviewer types
    
    def _predict_interviewer_focus(self, interviewer: Dict) -> List[str]:
        """Predict what an interviewer will focus on based on their role."""
        title = interviewer.get("title", "").lower()
        
        focus_areas = {
            "engineering": ["Technical depth", "Requirement clarity", "Development process"],
            "design": ["User empathy", "Design collaboration", "User research"],
            "product": ["Strategic thinking", "Prioritization", "Execution"],
            "ceo": ["Vision alignment", "Leadership", "Business impact"],
            "vp": ["Strategic planning", "Cross-team collaboration", "Scalability"]
        }
        
        for role_type, areas in focus_areas.items():
            if role_type in title:
                return areas
        
        return ["General competence", "Cultural fit", "Communication"]
    
    def _generate_interviewer_prep_notes(self, interviewer: Dict) -> List[str]:
        """Generate preparation notes for specific interviewer."""
        title = interviewer.get("title", "").lower()
        
        if "engineering" in title:
            return [
                "Prepare technical examples with clear requirements",
                "Discuss your approach to working with engineering teams",
                "Be ready to talk about data and metrics"
            ]
        elif "design" in title:
            return [
                "Emphasize user research and empathy",
                "Discuss design collaboration experiences", 
                "Prepare examples of user-centered decision making"
            ]
        elif "ceo" in title or "founder" in title:
            return [
                "Focus on strategic thinking and business impact",
                "Prepare vision and leadership examples",
                "Discuss company mission alignment"
            ]
        else:
            return [
                "Prepare role-relevant examples",
                "Focus on collaboration and communication",
                "Be ready to discuss strategic thinking"
            ]
    
    def _generate_star_responses(self, role_title: str, question_bank: Dict,
                               research_data: Dict = None) -> Dict:
        """Generate STAR method responses for key questions."""
        # Load case stories from repository
        case_stories = self._load_case_stories()
        
        # Select most relevant questions for STAR preparation
        key_questions = question_bank.get("high_probability", [])
        key_questions.extend(question_bank.get("role_specific", [])[:5])
        
        star_responses = {
            "framework": self.star_framework,
            "prepared_responses": {},
            "case_story_mapping": {},
            "ai_coaching_prompts": []
        }
        
        for question in key_questions[:10]:  # Limit to top 10 questions
            # Find best case story for this question
            best_story = self._match_question_to_case_story(question, case_stories, role_title)
            
            if best_story:
                # Generate STAR response framework
                response_framework = self._create_star_response_framework(
                    question, best_story, role_title, research_data
                )
                
                star_responses["prepared_responses"][question] = response_framework
                star_responses["case_story_mapping"][question] = best_story["title"]
                
                # Generate AI coaching prompt
                coaching_prompt = self.ai_prompts["star_response_coach"].format(
                    key_skills_for_role=self._get_key_skills(role_title),
                    interview_question=question,
                    case_stories_summary=self._summarize_case_story(best_story)
                )
                
                star_responses["ai_coaching_prompts"].append({
                    "question": question,
                    "prompt": coaching_prompt
                })
        
        return star_responses
    
    def _load_case_stories(self) -> List[Dict]:
        """Load case stories from repository."""
        # This would parse the Case_Stories_Repository.md file
        # For now, return structured sample data matching the repository
        return [
            {
                "title": "Steamship Authority Booking System Optimization",
                "situation": "Ferry booking system faced significant challenges during peak travel seasons, leading to customer frustration and operational inefficiencies",
                "task": "Analyze current booking system pain points, conduct stakeholder research, and develop comprehensive improvement strategy",
                "action": "Conducted extensive interviews with seasonal residents, tourism businesses, operations staff, and IT stakeholders. Identified critical pain points including complex booking flows, pricing confusion, mobile experience limitations, and customer communication gaps",
                "results": "Delivered detailed stakeholder research findings with actionable insights, created comprehensive improvement roadmap with prioritized initiatives, established framework for enhanced customer experience",
                "skills": ["Stakeholder management", "User research", "Service design", "System optimization"],
                "quantified_outcomes": ["65% Customer Effort Score improvement", "Comprehensive stakeholder analysis across 4 user groups"],
                "industry": "Transportation",
                "complexity": "high"
            },
            {
                "title": "HP AI Companion Product Launch",
                "situation": "Hewlett-Packard needed rapid, user-focused development of AI Companion product from concept to market",
                "task": "Enable rapid product development by connecting market insights with user needs and validating assumptions",
                "action": "Connected market insights with user needs, questioned assumptions systematically, enabled user-focused development process",
                "results": "Successful product launch within one month from initial research to market delivery",
                "skills": ["AI product development", "Market research", "Product strategy", "Rapid execution"],
                "quantified_outcomes": ["30-day concept-to-market timeline", "Successful product launch"],
                "industry": "Technology",
                "complexity": "high"
            },
            {
                "title": "Form Health Conversion Optimization",
                "situation": "Form Health, a consumer health startup, needed to improve their freemium-to-premium conversion rate",
                "task": "Formulate paid acquisition strategy and redesign onboarding funnel to improve conversion rates",
                "action": "Analyzed user acquisition funnel, redesigned onboarding experience, implemented systematic A/B testing program",
                "results": "Doubled conversion rate from 3.8% to 8.4%, acquired first 500+ paying customers",
                "skills": ["Growth strategy", "A/B testing", "Conversion optimization", "User acquisition"],
                "quantified_outcomes": ["8.4% final conversion rate", "3.8% to 8.4% improvement", "500+ paying customers"],
                "industry": "Healthcare",
                "complexity": "medium"
            },
            {
                "title": "Wasabi Technologies Growth Engine",
                "situation": "Wasabi Technologies needed to scale organic traffic and improve conversion rates for their enterprise B2B SaaS platform",
                "task": "Establish experimentation program and grow organic traffic from minimal to significant scale",
                "action": "Created comprehensive SEO strategy, established A/B testing framework, implemented systematic content and technical optimizations",
                "results": "Grew organic traffic from <100 to 10,000+ monthly visitors in 4 months, increased free trial conversion rate from 2.7% to 4.4% (+63%)",
                "skills": ["SEO strategy", "A/B testing", "Growth marketing", "B2B SaaS"],
                "quantified_outcomes": ["10,000+ monthly visitors", "2.7% to 4.4% conversion improvement", "63% conversion increase"],
                "industry": "Technology",
                "complexity": "medium"
            },
            {
                "title": "Vestis Enterprise Experimentation Program",
                "situation": "Vestis Uniforms (formerly Aramark Uniforms) needed to increase sales leads through systematic experimentation",
                "task": "Manage product analyst and create experimentation program to drive lead generation",
                "action": "Managed product analyst, designed and implemented systematic experimentation framework, optimized lead generation processes",
                "results": "46% increase in new sales leads through systematic experimentation program",
                "skills": ["People management", "Experimentation", "B2B sales", "Lead optimization"],
                "quantified_outcomes": ["46% increase in sales leads", "Managed 1 product analyst"],
                "industry": "B2B Services",
                "complexity": "medium"
            }
        ]
    
    def _match_question_to_case_story(self, question: str, case_stories: List[Dict], 
                                    role_title: str) -> Optional[Dict]:
        """Match interview question to most relevant case story."""
        question_lower = question.lower()
        
        # Question type mapping
        question_keywords = {
            "difficult decision": ["decision", "choice", "prioritization"],
            "influence without authority": ["influence", "stakeholder", "alignment"],
            "pivot": ["pivot", "change", "adaptation"], 
            "disagreement": ["disagreement", "conflict", "stakeholder"],
            "failed project": ["failure", "challenge", "problem"],
            "growth": ["growth", "scale", "acquisition", "conversion"],
            "prioritization": ["prioritize", "roadmap", "feature"],
            "data": ["data", "analytics", "metrics", "testing"],
            "team leadership": ["leadership", "management", "team"]
        }
        
        # Score each case story against the question
        best_story = None
        best_score = 0
        
        for story in case_stories:
            score = 0
            story_text = f"{story['situation']} {story['task']} {story['action']} {story['results']}".lower()
            
            # Check keyword matches
            for keyword_group in question_keywords.values():
                for keyword in keyword_group:
                    if keyword in question_lower and keyword in story_text:
                        score += 1
            
            # Bonus for quantified outcomes
            if story.get("quantified_outcomes"):
                score += 1
            
            # Role-specific bonus
            role_lower = role_title.lower()
            if "growth" in role_lower and "conversion" in story_text:
                score += 2
            elif "senior" in role_lower and story.get("complexity") == "high":
                score += 1
            
            if score > best_score:
                best_score = score
                best_story = story
        
        return best_story
    
    def _create_star_response_framework(self, question: str, case_story: Dict,
                                      role_title: str, research_data: Dict = None) -> Dict:
        """Create STAR response framework for a question using a case story."""
        return {
            "question": question,
            "case_story_used": case_story["title"],
            "star_framework": {
                "situation": {
                    "content": case_story["situation"],
                    "talking_points": [
                        "Set clear context and background",
                        "Mention company/project scale if relevant",
                        "Highlight why this was challenging/important"
                    ],
                    "time_allocation": "30 seconds"
                },
                "task": {
                    "content": case_story["task"],
                    "talking_points": [
                        "Clearly define your responsibility",
                        "Explain what success looked like",
                        "Mention constraints or challenges"
                    ],
                    "time_allocation": "45 seconds"
                },
                "action": {
                    "content": case_story["action"],
                    "talking_points": [
                        "Detail specific steps YOU took (not team)",
                        "Explain your decision-making process",
                        "Highlight relevant skills and approaches"
                    ],
                    "time_allocation": "60-90 seconds"
                },
                "result": {
                    "content": case_story["results"],
                    "talking_points": [
                        "Lead with quantified outcomes",
                        "Connect to business impact",
                        "Mention what you learned"
                    ],
                    "time_allocation": "30-45 seconds",
                    "quantified_outcomes": case_story.get("quantified_outcomes", [])
                }
            },
            "key_skills_demonstrated": case_story.get("skills", []),
            "practice_notes": [
                f"Practice timing - aim for 2-3 minutes total",
                f"Emphasize {', '.join(case_story.get('skills', [])[:3])}",
                "Connect outcomes to role requirements",
                "Be prepared for follow-up questions on methodology"
            ],
            "connection_to_role": self._connect_story_to_role(case_story, role_title)
        }
    
    def _get_key_skills(self, role_title: str) -> str:
        """Get key skills to emphasize for the role."""
        role_lower = role_title.lower()
        
        if "growth" in role_lower:
            return "growth strategy, experimentation, conversion optimization, user acquisition"
        elif "senior" in role_lower:
            return "strategic thinking, stakeholder management, cross-functional leadership, execution"
        elif "principal" in role_lower:
            return "vision setting, technical leadership, organizational influence, mentoring"
        else:
            return "product strategy, user research, data analysis, problem solving"
    
    def _summarize_case_story(self, case_story: Dict) -> str:
        """Create brief summary of case story for AI prompt."""
        return f"""Title: {case_story['title']}
Situation: {case_story['situation'][:100]}...
Key Results: {', '.join(case_story.get('quantified_outcomes', [])[:2])}
Skills: {', '.join(case_story.get('skills', [])[:3])}"""
    
    def _connect_story_to_role(self, case_story: Dict, role_title: str) -> str:
        """Explain how the case story connects to the target role."""
        role_lower = role_title.lower()
        story_skills = case_story.get("skills", [])
        
        connections = []
        
        if "growth" in role_lower and any("growth" in skill.lower() or "conversion" in skill.lower() for skill in story_skills):
            connections.append("Demonstrates systematic approach to growth and conversion optimization")
        
        if ("senior" in role_lower or "principal" in role_lower) and case_story.get("complexity") == "high":
            connections.append("Shows ability to handle complex, high-stakes projects")
        
        if "stakeholder" in " ".join(story_skills).lower():
            connections.append("Illustrates stakeholder management and alignment skills")
        
        if case_story.get("quantified_outcomes"):
            connections.append("Provides concrete metrics demonstrating business impact")
        
        return "; ".join(connections) if connections else "Relevant experience for role requirements"
    
    def _generate_talking_points(self, company_name: str, role_title: str,
                               research_data: Dict = None) -> Dict:
        """Generate company-specific talking points and value propositions."""
        talking_points = {
            "company_knowledge": self._generate_company_knowledge_points(company_name, research_data),
            "value_propositions": self._generate_value_propositions(role_title, research_data),
            "strategic_insights": self._generate_strategic_insights(company_name, research_data),
            "ai_talking_points_prompt": self.ai_prompts["company_talking_points"].format(
                company_name=company_name
            ),
            "conversation_starters": self._generate_conversation_starters(company_name, research_data)
        }
        
        return talking_points
    
    def _generate_company_knowledge_points(self, company_name: str,
                                         research_data: Dict = None) -> List[str]:
        """Generate talking points that demonstrate company knowledge."""
        points = [
            f"I've been following {company_name}'s growth and am impressed by [specific recent achievement]",
            f"Your mission to [company mission] resonates with my experience in [relevant area]",
            f"I'm particularly interested in how {company_name} is approaching [strategic priority]"
        ]
        
        if research_data:
            if "recent_news" in research_data:
                points.append(f"I saw {company_name}'s recent {research_data['recent_news']} - this aligns with trends I've seen in [relevant experience]")
            
            if "competitive_landscape" in research_data:
                points.append(f"Your differentiation from competitors through [specific advantage] is compelling")
        
        return points
    
    def _generate_value_propositions(self, role_title: str, research_data: Dict = None) -> List[str]:
        """Generate value propositions specific to the role."""
        base_props = [
            "Proven track record of delivering measurable business outcomes through systematic experimentation",
            "Experience scaling products from early stage to significant user bases",
            "Strong background in both B2B and B2C contexts with cross-functional team leadership"
        ]
        
        role_lower = role_title.lower()
        
        if "growth" in role_lower:
            base_props.extend([
                "Doubled conversion rates through systematic A/B testing and funnel optimization",
                "Experience launching AI-powered products from research to market in 30 days"
            ])
        elif "senior" in role_lower or "principal" in role_lower:
            base_props.extend([
                "Led complex stakeholder alignment initiatives across competing departmental goals",
                "Managed product analysts and built systematic experimentation programs"
            ])
        
        return base_props[:5]
    
    def _generate_strategic_insights(self, company_name: str, 
                                   research_data: Dict = None) -> List[str]:
        """Generate strategic insights about the company."""
        insights = [
            f"The opportunity for {company_name} to leverage AI/automation for product development",
            f"Potential for systematic experimentation to optimize key business metrics",
            f"Growth opportunities through improved user onboarding and conversion funnels"
        ]
        
        if research_data:
            if "key_challenges" in research_data:
                insights.append(f"Strategic approach to addressing {research_data['key_challenges']} through [specific methodology]")
            
            if "competitive_landscape" in research_data:
                insights.append(f"Differentiation opportunities in [specific area] based on competitive analysis")
        
        return insights
    
    def _generate_conversation_starters(self, company_name: str,
                                      research_data: Dict = None) -> List[str]:
        """Generate conversation starters that demonstrate strategic thinking."""
        starters = [
            f"I'm curious about {company_name}'s approach to [specific challenge] - in my experience with similar situations...",
            f"How is the product team thinking about [strategic opportunity]? I've seen interesting approaches to this at...",
            f"What's the biggest product challenge you're facing right now? I have some thoughts on [relevant methodology]..."
        ]
        
        return starters
    
    def _generate_interviewer_questions(self, company_name: str, role_title: str,
                                      research_data: Dict = None) -> Dict:
        """Generate thoughtful questions to ask interviewers."""
        questions = {
            "about_role": [
                f"What does success look like in this {role_title} role after 6 months?",
                "What are the biggest challenges facing this product area right now?",
                "How is the product team structured and who would I collaborate with most closely?",
                "What opportunities exist for professional growth and advancement?"
            ],
            "about_company": [
                f"How does {company_name} approach product experimentation and testing?",
                "What's the company's strategy for the next 12-18 months?",
                f"How has {company_name} evolved its product development process as it's scaled?",
                "What do you enjoy most about working here?"
            ],
            "about_team": [
                "How does the product team collaborate with engineering and design?",
                "What's the decision-making process for product priorities?",
                "How does the team handle disagreements or conflicting priorities?",
                "What tools and processes does the product team use?"
            ],
            "strategic": [
                f"How is {company_name} thinking about AI integration in its products?",
                "What role does user research play in product decisions?",
                "How do you measure product success and team performance?",
                "What's the biggest opportunity for product innovation here?"
            ]
        }
        
        # Add company-specific questions based on research
        if research_data:
            company_specific = []
            
            if "key_challenges" in research_data:
                company_specific.append(f"How is the team approaching {research_data['key_challenges']}?")
            
            if "recent_news" in research_data:
                company_specific.append(f"How will {research_data['recent_news']} impact product strategy?")
            
            if company_specific:
                questions["company_specific"] = company_specific
        
        return questions
    
    def _create_mock_scenarios(self, company_name: str, role_title: str,
                             question_bank: Dict) -> Dict:
        """Create mock interview scenarios for practice."""
        scenarios = {
            "scenario_1": {
                "name": "Technical Deep Dive",
                "duration": "45 minutes",
                "interviewer_profile": "Engineering Manager",
                "focus": "Technical competence and collaboration",
                "questions": [
                    "Walk me through how you would approach [specific technical challenge]",
                    "How do you work with engineering teams to scope projects?",
                    "Tell me about your experience with data analysis and SQL",
                    "How do you ensure product requirements are clearly communicated?"
                ]
            },
            "scenario_2": {
                "name": "Strategic Thinking",
                "duration": "45 minutes", 
                "interviewer_profile": "Head of Product",
                "focus": "Strategic planning and execution",
                "questions": [
                    "How would you prioritize our product roadmap?",
                    "Tell me about a time you had to make a difficult product decision",
                    "How do you balance technical debt vs. new features?",
                    "Walk me through your framework for entering new markets"
                ]
            },
            "scenario_3": {
                "name": "Behavioral Interview",
                "duration": "30 minutes",
                "interviewer_profile": "Peer Product Manager", 
                "focus": "Collaboration and problem-solving",
                "questions": [
                    "Tell me about a time when you had to influence someone without authority",
                    "Describe a project that didn't go as planned",
                    "How do you handle conflicting stakeholder priorities?",
                    "Tell me about your biggest professional failure"
                ]
            }
        }
        
        return scenarios
    
    def _generate_ai_prep_prompts(self, company_name: str, role_title: str) -> List[Dict]:
        """Generate AI prompts for additional interview preparation."""
        return [
            {
                "purpose": "Additional Question Generation",
                "prompt": f"Generate 10 additional interview questions for a {role_title} role at {company_name}, focusing on scenarios I might not have considered. Include both behavioral and situational questions.",
                "usage": "Use to expand question preparation beyond the generated question bank"
            },
            {
                "purpose": "Mock Interview Practice",
                "prompt": f"Act as a hiring manager at {company_name} interviewing for a {role_title} position. Ask me challenging questions and provide feedback on my responses.",
                "usage": "Practice interview responses with AI feedback"
            },
            {
                "purpose": "Company-Specific Insights",
                "prompt": f"Based on current market conditions and {company_name}'s position, what are the key strategic challenges a {role_title} should be prepared to discuss?",
                "usage": "Deepen company-specific strategic preparation"
            }
        ]
    
    def _generate_prep_checklist(self) -> Dict:
        """Generate comprehensive interview preparation checklist."""
        return {
            "research_preparation": [
                "Complete company research using AI prompts",
                "Research interviewer backgrounds on LinkedIn",
                "Review recent company news and developments",
                "Understand product portfolio and competitive landscape",
                "Practice company-specific talking points"
            ],
            "response_preparation": [
                "Practice STAR responses for high-probability questions",
                "Prepare 3-5 case stories with quantified outcomes",
                "Practice explaining technical concepts clearly",
                "Prepare examples for each key competency",
                "Practice connecting experiences to role requirements"
            ],
            "logistics_preparation": [
                "Test video call technology and setup",
                "Prepare backup internet connection",
                "Set up quiet, professional environment",
                "Prepare copies of resume and portfolio materials",
                "Plan arrival time and route (if in-person)"
            ],
            "day_of_interview": [
                "Review key talking points and value propositions",
                "Practice elevator pitch and company knowledge points",
                "Prepare thoughtful questions for each interviewer",
                "Bring notebook for taking notes",
                "Follow up within 24 hours with thank you notes"
            ]
        }
    
    def _save_interview_prep(self, prep_package: Dict) -> Path:
        """Save comprehensive interview prep materials to company folder."""
        company_name = prep_package["company_name"]
        company_key = company_name.lower().replace(" ", "_")
        company_dir = self.output_dir / company_key
        company_dir.mkdir(parents=True, exist_ok=True)
        
        # Main interview prep guide
        prep_file = company_dir / f"{company_name.replace(' ', '_')}_Interview_Preparation_Guide.md"
        
        prep_content = f"""# Interview Preparation Guide - {company_name}

**Role:** {prep_package['role_title']}  
**Preparation Date:** {prep_package['prep_date']}

---

## Preparation Overview

This comprehensive guide contains AI-generated interview materials, STAR method responses, and company-specific talking points to ensure superior interview performance.

**Preparation Time Required:** 4-6 hours  
**Success Target:** Demonstrate deeper company knowledge than typical candidates

---

## Question Bank

{self._format_question_bank(prep_package['question_bank'])}

---

## STAR Method Responses

{self._format_star_responses(prep_package['star_responses'])}

---

## Company-Specific Talking Points

{self._format_talking_points(prep_package['talking_points'])}

---

## Questions to Ask Interviewers

{self._format_interviewer_questions(prep_package['interviewer_questions'])}

---

## Interviewer Analysis

{self._format_interviewer_analysis(prep_package['interviewer_analysis'])}

---

## Mock Interview Scenarios

{self._format_mock_scenarios(prep_package['mock_scenarios'])}

---

## AI Preparation Prompts

{self._format_ai_prep_prompts(prep_package['ai_prep_prompts'])}

---

## Preparation Checklist

{self._format_prep_checklist(prep_package['preparation_checklist'])}

---

## Success Metrics

Track your interview performance:
- [ ] Demonstrated superior company knowledge
- [ ] Asked thoughtful, strategic questions
- [ ] Provided specific, quantified examples
- [ ] Connected experience to role requirements
- [ ] Received positive feedback on preparation level
"""
        
        with open(prep_file, 'w') as f:
            f.write(prep_content)
        
        logger.info(f"Interview prep guide saved to: {prep_file}")
        return prep_file
    
    def _format_question_bank(self, question_bank: Dict) -> str:
        """Format question bank for markdown display."""
        formatted = "### High-Probability Questions\n\n"
        
        for question in question_bank.get("high_probability", []):
            formatted += f"- {question}\n"
        
        formatted += "\n### Role-Specific Questions\n\n"
        
        for question in question_bank.get("role_specific", [])[:10]:
            formatted += f"- {question}\n"
        
        formatted += "\n### AI Question Generation\n\n"
        ai_predictions = question_bank.get("ai_predictions", {})
        if ai_predictions.get("prompt_for_execution"):
            formatted += "**AI Prompt for Additional Questions:**\n```\n"
            formatted += ai_predictions["prompt_for_execution"]
            formatted += "\n```\n"
        
        return formatted
    
    def _format_star_responses(self, star_responses: Dict) -> str:
        """Format STAR responses for markdown display."""
        formatted = "### Framework Overview\n\n"
        
        framework = star_responses.get("framework", {})
        if framework.get("definition"):
            for element, definition in framework["definition"].items():
                formatted += f"**{element}:** {definition}\n\n"
        
        formatted += "\n### Prepared Responses\n\n"
        
        responses = star_responses.get("prepared_responses", {})
        for i, (question, response) in enumerate(responses.items(), 1):
            if i > 5:  # Limit to top 5 for display
                break
                
            formatted += f"#### {i}. {question}\n\n"
            formatted += f"**Case Story:** {response.get('case_story_used', 'TBD')}\n\n"
            
            framework = response.get("star_framework", {})
            for element in ["situation", "task", "action", "result"]:
                if element in framework:
                    formatted += f"**{element.title()}** ({framework[element].get('time_allocation', 'N/A')}):\n"
                    formatted += f"{framework[element].get('content', 'TBD')}\n\n"
            
            formatted += "---\n\n"
        
        return formatted
    
    def _format_talking_points(self, talking_points: Dict) -> str:
        """Format talking points for markdown display."""
        formatted = ""
        
        sections = [
            ("company_knowledge", "Company Knowledge Points"),
            ("value_propositions", "Value Propositions"),
            ("strategic_insights", "Strategic Insights"),
            ("conversation_starters", "Conversation Starters")
        ]
        
        for key, title in sections:
            if key in talking_points:
                formatted += f"### {title}\n\n"
                points = talking_points[key]
                if isinstance(points, list):
                    for point in points:
                        formatted += f"- {point}\n"
                else:
                    formatted += f"{points}\n"
                formatted += "\n"
        
        return formatted
    
    def _format_interviewer_questions(self, interviewer_questions: Dict) -> str:
        """Format questions to ask interviewers."""
        formatted = ""
        
        for category, questions in interviewer_questions.items():
            category_title = category.replace("_", " ").title()
            formatted += f"### {category_title}\n\n"
            
            for question in questions:
                formatted += f"- {question}\n"
            formatted += "\n"
        
        return formatted
    
    def _format_interviewer_analysis(self, interviewer_analysis: Dict) -> str:
        """Format interviewer analysis for display."""
        formatted = "### Interviewer Profiles\n\n"
        
        profiles = interviewer_analysis.get("profiles", [])
        for profile in profiles:
            formatted += f"#### {profile['name']} - {profile['title']}\n\n"
            formatted += f"**Background:** {profile['background']}\n"
            formatted += f"**Focus Areas:** {', '.join(profile.get('likely_focus_areas', []))}\n\n"
            
            prep_notes = profile.get("preparation_notes", [])
            if prep_notes:
                formatted += "**Preparation Notes:**\n"
                for note in prep_notes:
                    formatted += f"- {note}\n"
            
            formatted += "\n---\n\n"
        
        return formatted
    
    def _format_mock_scenarios(self, mock_scenarios: Dict) -> str:
        """Format mock interview scenarios."""
        formatted = ""
        
        for scenario_key, scenario in mock_scenarios.items():
            formatted += f"### {scenario['name']}\n\n"
            formatted += f"**Duration:** {scenario['duration']}\n"
            formatted += f"**Interviewer:** {scenario['interviewer_profile']}\n"
            formatted += f"**Focus:** {scenario['focus']}\n\n"
            
            formatted += "**Questions:**\n"
            for question in scenario['questions']:
                formatted += f"- {question}\n"
            
            formatted += "\n---\n\n"
        
        return formatted
    
    def _format_ai_prep_prompts(self, ai_prompts: List[Dict]) -> str:
        """Format AI preparation prompts."""
        formatted = ""
        
        for prompt in ai_prompts:
            formatted += f"### {prompt['purpose']}\n\n"
            formatted += "**Prompt:**\n```\n"
            formatted += prompt['prompt']
            formatted += "\n```\n\n"
            formatted += f"**Usage:** {prompt['usage']}\n\n"
            formatted += "---\n\n"
        
        return formatted
    
    def _format_prep_checklist(self, checklist: Dict) -> str:
        """Format preparation checklist."""
        formatted = ""
        
        for category, items in checklist.items():
            category_title = category.replace("_", " ").title()
            formatted += f"### {category_title}\n\n"
            
            for item in items:
                formatted += f"- [ ] {item}\n"
            formatted += "\n"
        
        return formatted

# Example usage
if __name__ == "__main__":
    prep_system = InterviewPrepSystem()
    
    # Example interview preparation
    prep_materials = prep_system.generate_interview_prep(
        company_name="Canva",
        role_title="Senior Product Manager", 
        research_data={
            "key_challenges": "scaling AI adoption",
            "recent_news": "AI-powered design features launch",
            "competitive_landscape": "competing with Adobe and Figma"
        }
    )
    
    print(f"✅ Interview prep materials generated for {prep_materials['company_name']}")
    print(f"📋 {len(prep_materials['question_bank']['high_probability'])} high-priority questions prepared")
    print(f"⭐ {len(prep_materials['star_responses']['prepared_responses'])} STAR responses created")