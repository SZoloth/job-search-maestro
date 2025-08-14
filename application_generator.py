#!/usr/bin/env python3
"""
Dynamic Application Package Generator

Automated generation of customized application materials including:
- Role-specific resume optimization
- Company-tailored cover letters  
- Relevant case story compilation
- Application tracking documentation

This system implements Sam's proven application methodology:
- Keyword optimization from job descriptions
- Experience reframing for maximum relevance
- Value proposition customization
- Company-specific personalization

Usage:
    from application_generator import ApplicationGenerator
    
    generator = ApplicationGenerator()
    package = generator.generate_application_package("Canva", "Senior Product Manager")
"""

import json
import re
from datetime import datetime
from typing import Dict, List, Optional, Set
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class ApplicationGenerator:
    """
    Dynamic application package generator for customized job applications.
    
    Generates three core components:
    1. Company-specific resume with keyword optimization
    2. Tailored cover letter with research-based personalization  
    3. Relevant case story collection with STAR formatting
    
    All materials are customized based on:
    - Job description analysis and keyword extraction
    - Company research findings
    - Role-specific experience highlighting
    - Strategic positioning for maximum impact
    """
    
    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.templates_dir = Path("templates")
        self.case_stories_dir = Path("experience")
        self.output_dir = Path("Applications")
        
        # Load base templates and case stories
        self.base_resume = self._load_base_resume()
        self.cover_letter_template = self._load_cover_letter_template()
        self.case_stories = self._load_case_stories()
        
        # Initialize keyword extraction and optimization
        self.skill_keywords = self._load_skill_keywords()
        self.industry_keywords = self._load_industry_keywords()
    
    def generate_application_package(self, company_name: str, role_title: str,
                                   job_description: str = None, 
                                   research_data: Dict = None) -> Dict:
        """
        Generate complete application package for a specific company and role.
        
        Phase 3: Application Customization (90-120 minutes automated)
        
        Args:
            company_name: Target company name
            role_title: Target role title
            job_description: Job posting text (optional)
            research_data: Company research findings (optional)
            
        Returns:
            Dictionary containing all generated application materials
        """
        logger.info(f"Generating application package for {company_name} - {role_title}")
        
        # Extract keywords and requirements from job description
        job_analysis = self._analyze_job_description(job_description) if job_description else {}
        
        # Generate customized resume
        logger.info("Generating customized resume...")
        resume = self._generate_customized_resume(
            company_name, role_title, job_analysis, research_data
        )
        
        # Generate tailored cover letter
        logger.info("Generating tailored cover letter...")
        cover_letter = self._generate_cover_letter(
            company_name, role_title, job_analysis, research_data
        )
        
        # Select and format relevant case stories
        logger.info("Selecting relevant case stories...")
        case_stories = self._select_relevant_case_stories(
            role_title, job_analysis, limit=5
        )
        
        # Create application package
        application_package = {
            "company_name": company_name,
            "role_title": role_title,
            "generation_date": datetime.now().isoformat(),
            "job_analysis": job_analysis,
            "resume": resume,
            "cover_letter": cover_letter,
            "case_stories": case_stories,
            "optimization_summary": self._generate_optimization_summary(
                company_name, role_title, job_analysis
            )
        }
        
        # Save application package to company folder
        self._save_application_package(application_package)
        
        logger.info(f"Application package generated for {company_name}")
        return application_package
    
    def _analyze_job_description(self, job_description: str) -> Dict:
        """
        Analyze job description to extract keywords, requirements, and priorities.
        
        Implements keyword optimization strategy:
        - Extract key terms and skills
        - Identify required vs. preferred qualifications
        - Determine role priorities and focus areas
        - Map to existing experience and capabilities
        """
        if not job_description:
            return {}
        
        # Clean and normalize text
        text = re.sub(r'\s+', ' ', job_description.lower())
        
        # Extract key sections
        sections = self._extract_job_sections(job_description)
        
        # Extract keywords by category
        keywords = {
            "technical_skills": self._extract_technical_keywords(text),
            "soft_skills": self._extract_soft_skills_keywords(text),
            "experience_keywords": self._extract_experience_keywords(text),
            "industry_terms": self._extract_industry_keywords(text),
            "tools_platforms": self._extract_tools_keywords(text)
        }
        
        # Identify requirements vs. preferences
        requirements = self._classify_requirements(sections)
        
        # Extract key metrics and outcomes mentioned
        success_metrics = self._extract_success_metrics(text)
        
        return {
            "sections": sections,
            "keywords": keywords,
            "requirements": requirements,
            "success_metrics": success_metrics,
            "keyword_count": sum(len(v) for v in keywords.values()),
            "analysis_summary": self._generate_job_analysis_summary(keywords, requirements)
        }
    
    def _extract_job_sections(self, job_description: str) -> Dict[str, str]:
        """Extract key sections from job description."""
        sections = {}
        
        # Common section patterns
        section_patterns = {
            "responsibilities": r"(?:responsibilities|duties|role|what you'll do)[:\n](.+?)(?=\n\n|\n[A-Z]|requirements|qualifications|$)",
            "requirements": r"(?:requirements|qualifications|what you need|must have)[:\n](.+?)(?=\n\n|\n[A-Z]|nice to have|preferred|$)",
            "preferred": r"(?:nice to have|preferred|bonus|plus)[:\n](.+?)(?=\n\n|\n[A-Z]|benefits|about|$)",
            "about_company": r"(?:about|company|who we are)[:\n](.+?)(?=\n\n|\n[A-Z]|role|responsibilities|$)"
        }
        
        for section_name, pattern in section_patterns.items():
            match = re.search(pattern, job_description, re.IGNORECASE | re.DOTALL)
            if match:
                sections[section_name] = match.group(1).strip()
        
        return sections
    
    def _extract_technical_keywords(self, text: str) -> List[str]:
        """Extract technical skills and technologies."""
        technical_terms = [
            # Product Management
            "product management", "product strategy", "roadmapping", "user stories",
            "agile", "scrum", "kanban", "sprint planning", "backlog management",
            "okrs", "kpis", "metrics", "analytics", "a/b testing", "experimentation",
            
            # Data & Analytics  
            "sql", "python", "r", "excel", "tableau", "amplitude", "mixpanel",
            "google analytics", "data analysis", "statistical analysis",
            
            # Design & UX
            "user research", "usability testing", "personas", "user journeys",
            "wireframing", "prototyping", "design thinking", "ux design",
            
            # Technical
            "apis", "rest", "graphql", "json", "databases", "cloud", "aws", "gcp",
            "machine learning", "ai", "artificial intelligence", "automation",
            
            # Growth & Marketing
            "growth hacking", "conversion optimization", "funnel analysis",
            "cohort analysis", "retention", "churn", "ltv", "cac"
        ]
        
        found_keywords = []
        for term in technical_terms:
            if term in text:
                found_keywords.append(term)
        
        return found_keywords
    
    def _extract_soft_skills_keywords(self, text: str) -> List[str]:
        """Extract soft skills and competencies."""
        soft_skills = [
            "leadership", "communication", "collaboration", "teamwork",
            "problem solving", "analytical thinking", "strategic thinking",
            "project management", "stakeholder management", "influence",
            "mentoring", "coaching", "facilitation", "presentation skills"
        ]
        
        found_keywords = []
        for skill in soft_skills:
            if skill in text:
                found_keywords.append(skill)
        
        return found_keywords
    
    def _extract_experience_keywords(self, text: str) -> List[str]:
        """Extract experience-related keywords."""
        experience_terms = [
            "years experience", "senior level", "lead", "director", "manager",
            "b2b", "b2c", "saas", "enterprise", "startup", "scale-up",
            "consumer", "mobile", "web", "platform", "marketplace",
            "fintech", "healthtech", "edtech", "e-commerce"
        ]
        
        found_keywords = []
        for term in experience_terms:
            if term in text:
                found_keywords.append(term)
        
        return found_keywords
    
    def _extract_industry_keywords(self, text: str) -> List[str]:
        """Extract industry-specific terms."""
        # This would be expanded based on target industries
        industry_terms = [
            "healthcare", "medical", "telemedicine", "digital health",
            "education", "learning", "training", "curriculum",
            "financial services", "payments", "banking", "insurance",
            "retail", "e-commerce", "marketplace", "consumer goods"
        ]
        
        found_keywords = []
        for term in industry_terms:
            if term in text:
                found_keywords.append(term)
        
        return found_keywords
    
    def _extract_tools_keywords(self, text: str) -> List[str]:
        """Extract specific tools and platforms."""
        tools = [
            "jira", "asana", "trello", "notion", "confluence",
            "figma", "sketch", "adobe", "canva",
            "salesforce", "hubspot", "intercom", "zendesk",
            "slack", "teams", "zoom", "github", "gitlab"
        ]
        
        found_keywords = []
        for tool in tools:
            if tool in text:
                found_keywords.append(tool)
        
        return found_keywords
    
    def _classify_requirements(self, sections: Dict[str, str]) -> Dict[str, List[str]]:
        """Classify requirements as must-have vs. nice-to-have."""
        requirements_text = sections.get("requirements", "")
        preferred_text = sections.get("preferred", "")
        
        # Split into bullet points or sentences
        must_have = self._extract_bullet_points(requirements_text)
        nice_to_have = self._extract_bullet_points(preferred_text)
        
        return {
            "must_have": must_have,
            "nice_to_have": nice_to_have
        }
    
    def _extract_bullet_points(self, text: str) -> List[str]:
        """Extract bullet points from text."""
        if not text:
            return []
        
        # Split on bullet point indicators
        bullets = re.split(r'[•\-\*]\s*|^\d+\.\s*', text, flags=re.MULTILINE)
        bullets = [b.strip() for b in bullets if b.strip()]
        
        return bullets[:10]  # Limit to prevent excessive length
    
    def _extract_success_metrics(self, text: str) -> List[str]:
        """Extract mentioned success metrics and KPIs."""
        metric_patterns = [
            r'(\d+[%+]?\s*(?:increase|growth|improvement))',
            r'(\d+[%+]?\s*(?:conversion|retention|engagement))',
            r'(\$\d+[kmb]?\s*(?:revenue|arr|mrr))',
            r'(\d+[%+]?\s*(?:reduction|decrease)\s+in\s+\w+)'
        ]
        
        metrics = []
        for pattern in metric_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            metrics.extend(matches)
        
        return metrics[:5]  # Limit to most relevant
    
    def _generate_job_analysis_summary(self, keywords: Dict, requirements: Dict) -> str:
        """Generate summary of job analysis findings."""
        total_keywords = sum(len(v) for v in keywords.values())
        must_have_count = len(requirements.get("must_have", []))
        
        return f"Identified {total_keywords} relevant keywords and {must_have_count} key requirements"
    
    def _generate_customized_resume(self, company_name: str, role_title: str,
                                  job_analysis: Dict, research_data: Dict = None) -> Dict:
        """
        Generate company-specific resume with keyword optimization.
        
        Resume Optimization Strategy:
        - Keyword optimization from job analysis
        - Experience reframing for role relevance
        - Skills alignment with job requirements  
        - Company-specific terminology integration
        """
        # Load base resume structure
        resume = self.base_resume.copy()
        
        # Customize header and summary
        resume["header"] = self._customize_resume_header(company_name, role_title)
        resume["summary"] = self._customize_resume_summary(role_title, job_analysis)
        
        # Reframe experience for maximum relevance
        resume["experience"] = self._reframe_experience_section(role_title, job_analysis)
        
        # Optimize skills section
        resume["skills"] = self._optimize_skills_section(job_analysis)
        
        # Add relevant projects/achievements
        resume["projects"] = self._select_relevant_projects(role_title, job_analysis)
        
        # Generate optimization report
        resume["optimization_report"] = self._generate_resume_optimization_report(
            job_analysis, resume
        )
        
        return resume
    
    def _generate_cover_letter(self, company_name: str, role_title: str,
                             job_analysis: Dict, research_data: Dict = None) -> Dict:
        """
        Generate tailored cover letter with company-specific personalization.
        
        Cover Letter Strategy:
        - Opening hook with research-based personalization
        - Value proposition with 3-4 compelling points
        - Specific examples addressing company challenges
        - Clear call to action
        """
        # Research-based opening hook
        opening_hook = self._generate_opening_hook(company_name, research_data)
        
        # Core value proposition points
        value_propositions = self._generate_value_propositions(role_title, job_analysis)
        
        # Specific examples and evidence
        examples = self._select_cover_letter_examples(role_title, job_analysis)
        
        # Call to action
        call_to_action = self._generate_call_to_action(company_name, role_title)
        
        cover_letter = {
            "company_name": company_name,
            "role_title": role_title,
            "opening_hook": opening_hook,
            "value_propositions": value_propositions,
            "examples": examples,
            "call_to_action": call_to_action,
            "full_text": self._assemble_cover_letter(
                opening_hook, value_propositions, examples, call_to_action
            )
        }
        
        return cover_letter
    
    def _select_relevant_case_stories(self, role_title: str, job_analysis: Dict,
                                    limit: int = 5) -> List[Dict]:
        """
        Select most relevant case stories based on role and job requirements.
        
        Case Story Selection Criteria:
        - Skills match with job requirements
        - Industry relevance
        - Role level appropriateness
        - Outcome significance and measurability
        """
        if not self.case_stories:
            return []
        
        # Score case stories based on relevance
        scored_stories = []
        for story in self.case_stories:
            score = self._score_case_story_relevance(story, role_title, job_analysis)
            scored_stories.append((score, story))
        
        # Sort by score and return top stories
        scored_stories.sort(key=lambda x: x[0], reverse=True)
        selected_stories = [story for score, story in scored_stories[:limit]]
        
        return selected_stories
    
    def _score_case_story_relevance(self, story: Dict, role_title: str, 
                                  job_analysis: Dict) -> float:
        """Score case story relevance to role and job requirements."""
        score = 0.0
        
        # Keywords match
        keywords = job_analysis.get("keywords", {})
        story_text = json.dumps(story).lower()
        
        for category, keyword_list in keywords.items():
            for keyword in keyword_list:
                if keyword in story_text:
                    score += 1.0
        
        # Role-specific relevance
        role_keywords = self._get_role_specific_keywords(role_title)
        for keyword in role_keywords:
            if keyword in story_text:
                score += 2.0  # Higher weight for role-specific terms
        
        # Quantified outcomes bonus
        if any(char.isdigit() for char in story.get("results", "")):
            score += 1.5
        
        return score
    
    def _get_role_specific_keywords(self, role_title: str) -> List[str]:
        """Get keywords specific to the role type."""
        role_lower = role_title.lower()
        
        if "growth" in role_lower:
            return ["acquisition", "conversion", "retention", "engagement", "funnel", "a/b test"]
        elif "product" in role_lower:
            return ["roadmap", "feature", "user story", "sprint", "stakeholder", "metrics"]
        elif "strategy" in role_lower:
            return ["strategic", "planning", "analysis", "framework", "competitive"]
        else:
            return ["management", "leadership", "execution", "results", "improvement"]
    
    def _load_base_resume(self) -> Dict:
        """Load base resume template."""
        # This would load from a template file
        # For now, return a structured representation
        return {
            "header": {
                "name": "Sam Zoloth",
                "email": "zoloth@hey.com",
                "phone": "617-943-0717",
                "linkedin": "linkedin.com/in/samuelzoloth/"
            },
            "summary": "Product leader with 9+ years of experience driving business growth...",
            "experience": [
                {
                    "title": "Senior Product Strategist",
                    "company": "Stellar Elements, an Amdocs company",
                    "location": "Remote",
                    "dates": "January 2022 - Present",
                    "bullets": [
                        "Led end-to-end product specification for Steamship Authority's booking experience redesign...",
                        "Enabled rapid development of Hewlett-Packard's AI Companion...",
                        "Drove cross-functional alignment for $2B logistics company..."
                    ]
                }
            ],
            "skills": {
                "product_management": ["Product strategy", "Roadmapping", "User research"],
                "technical": ["SQL", "Python", "Analytics"],
                "tools": ["Amplitude", "Mixpanel", "Google Analytics"]
            }
        }
    
    def _load_cover_letter_template(self) -> str:
        """Load cover letter template."""
        return """Dear Hiring Manager,

{opening_hook}

{value_propositions}

{examples}

{call_to_action}

Best regards,
Sam Zoloth"""
    
    def _load_case_stories(self) -> List[Dict]:
        """Load case stories from the repository."""
        # This would load from the Case_Stories_Repository.md file
        # For now, return structured sample data
        return [
            {
                "title": "Steamship Authority Booking System Optimization",
                "situation": "Ferry booking system challenges during peak seasons",
                "task": "Improve user experience and operational efficiency",
                "action": "Conducted stakeholder research, identified pain points, developed improvement strategy",
                "results": "65% Customer Effort Score improvement through usability testing",
                "skills": ["User research", "Stakeholder management", "UX optimization"],
                "industry": "Transportation"
            },
            {
                "title": "HP AI Companion Product Launch",
                "situation": "Rapid development needed for AI-powered product",
                "task": "Enable user-focused development from concept to launch",
                "action": "Connected market insights with user needs, questioned assumptions",
                "results": "Successful product launch within one month",
                "skills": ["AI product development", "Market research", "Product strategy"],
                "industry": "Technology"
            }
        ]
    
    def _load_skill_keywords(self) -> Set[str]:
        """Load skill keyword database."""
        return set([
            "product management", "growth strategy", "user research", "analytics",
            "a/b testing", "agile", "scrum", "sql", "python", "leadership"
        ])
    
    def _load_industry_keywords(self) -> Dict[str, Set[str]]:
        """Load industry-specific keyword mappings."""
        return {
            "healthcare": {"telemedicine", "medical", "patient", "clinical"},
            "fintech": {"payments", "banking", "financial", "compliance"},
            "edtech": {"learning", "education", "curriculum", "students"}
        }
    
    def _customize_resume_header(self, company_name: str, role_title: str) -> Dict:
        """Customize resume header for specific application."""
        return {
            "name": "Sam Zoloth",
            "email": "zoloth@hey.com", 
            "phone": "617-943-0717",
            "linkedin": "linkedin.com/in/samuelzoloth/",
            "target_role": role_title,
            "target_company": company_name
        }
    
    def _customize_resume_summary(self, role_title: str, job_analysis: Dict) -> str:
        """Customize resume summary based on role and job analysis."""
        keywords = job_analysis.get("keywords", {})
        key_terms = []
        
        # Extract most relevant keywords
        for category, terms in keywords.items():
            key_terms.extend(terms[:3])  # Top 3 from each category
        
        # Generate role-specific summary
        if "growth" in role_title.lower():
            base_summary = "Growth-focused product leader with 9+ years of experience driving user acquisition, conversion optimization, and business expansion through data-driven experimentation and strategic product development."
        elif "senior" in role_title.lower():
            base_summary = "Senior product leader with 9+ years of experience leading cross-functional teams to deliver high-impact products through user-centered research, strategic planning, and systematic execution."
        else:
            base_summary = "Product leader with 9+ years of experience driving business growth through user-centered and AI-powered solutions, leveraging deep expertise in research, analytics, and experimentation."
        
        # Incorporate key terms naturally
        if key_terms:
            relevant_terms = key_terms[:5]  # Top 5 most relevant
            base_summary += f" Expertise in {', '.join(relevant_terms)} with a track record of delivering measurable outcomes."
        
        return base_summary
    
    def _reframe_experience_section(self, role_title: str, job_analysis: Dict) -> List[Dict]:
        """Reframe experience bullets for maximum relevance to role."""
        # This would take the base experience and reframe bullets
        # based on job analysis and role requirements
        
        experience_section = [
            {
                "title": "Senior Product Strategist", 
                "company": "Stellar Elements, an Amdocs company",
                "location": "Remote",
                "dates": "January 2022 - Present",
                "bullets": self._optimize_experience_bullets(
                    "current_role", role_title, job_analysis
                )
            }
        ]
        
        return experience_section
    
    def _optimize_experience_bullets(self, role_key: str, target_role: str, 
                                   job_analysis: Dict) -> List[str]:
        """Optimize experience bullets for target role."""
        # Get base bullets for the role
        base_bullets = {
            "current_role": [
                "Led end-to-end product specification for Steamship Authority's booking experience redesign, creating comprehensive PRD, user stories, and API architecture - delivering ahead of schedule with 65% Customer Effort Score improvement validated through usability testing",
                "Enabled rapid, user-focused development of Hewlett-Packard's AI Companion by connecting market insights with user needs and questioning assumptions, leading to successful product launch within one month",
                "Drove cross-functional alignment for $2B logistics company by transforming competing departmental goals into shared metrics framework, enabling product team to prioritize features that grew marketplace liquidity",
                "Developed and presented product strategies and go-to-market plans, pioneering use of AI-driven client research and quantitative growth models for 13 client pitches, resulting in over $13M in new business"
            ]
        }
        
        bullets = base_bullets.get(role_key, [])
        
        # Reorder bullets based on relevance to target role
        if "growth" in target_role.lower():
            # Prioritize growth-related bullets
            bullets = sorted(bullets, key=lambda b: (
                "growth" in b.lower() or "acquisition" in b.lower() or 
                "conversion" in b.lower() or "%" in b
            ), reverse=True)
        
        return bullets
    
    def _optimize_skills_section(self, job_analysis: Dict) -> Dict[str, List[str]]:
        """Optimize skills section based on job analysis."""
        keywords = job_analysis.get("keywords", {})
        
        # Base skills organized by category
        base_skills = {
            "Product Management": ["Product strategy", "Roadmapping", "User research", "Analytics"],
            "Technical Skills": ["SQL", "Python", "A/B testing", "Data analysis"],
            "Tools & Platforms": ["Amplitude", "Mixpanel", "Google Analytics", "Figma"]
        }
        
        # Prioritize skills mentioned in job description
        optimized_skills = {}
        for category, skills in base_skills.items():
            # Reorder skills based on keyword matches
            tech_keywords = keywords.get("technical_skills", [])
            tools_keywords = keywords.get("tools_platforms", [])
            
            relevant_skills = []
            other_skills = []
            
            for skill in skills:
                if (skill.lower() in tech_keywords or skill.lower() in tools_keywords):
                    relevant_skills.append(skill)
                else:
                    other_skills.append(skill)
            
            # Combine with relevant skills first
            optimized_skills[category] = relevant_skills + other_skills
        
        return optimized_skills
    
    def _select_relevant_projects(self, role_title: str, job_analysis: Dict) -> List[Dict]:
        """Select most relevant projects to highlight."""
        # This would select from a database of projects
        return [
            {
                "name": "AI-Powered Growth Optimization",
                "description": "Implemented systematic experimentation framework using AI tools",
                "relevance_score": 0.9
            }
        ]
    
    def _generate_resume_optimization_report(self, job_analysis: Dict, resume: Dict) -> Dict:
        """Generate optimization report showing keyword matches and improvements."""
        keywords = job_analysis.get("keywords", {})
        resume_text = json.dumps(resume).lower()
        
        matches = {}
        total_possible = 0
        total_matched = 0
        
        for category, keyword_list in keywords.items():
            category_matches = []
            for keyword in keyword_list:
                if keyword in resume_text:
                    category_matches.append(keyword)
                    total_matched += 1
                total_possible += 1
            
            matches[category] = {
                "matched": category_matches,
                "count": len(category_matches),
                "total": len(keyword_list)
            }
        
        match_percentage = (total_matched / total_possible * 100) if total_possible > 0 else 0
        
        return {
            "keyword_matches": matches,
            "overall_match_percentage": round(match_percentage, 1),
            "optimization_suggestions": self._generate_optimization_suggestions(matches)
        }
    
    def _generate_optimization_suggestions(self, matches: Dict) -> List[str]:
        """Generate suggestions for further resume optimization."""
        suggestions = []
        
        for category, match_data in matches.items():
            match_rate = match_data["count"] / match_data["total"] if match_data["total"] > 0 else 0
            
            if match_rate < 0.5:  # Less than 50% match rate
                suggestions.append(f"Consider adding more {category.replace('_', ' ')} keywords")
        
        return suggestions
    
    def _generate_opening_hook(self, company_name: str, research_data: Dict = None) -> str:
        """
        Generate research-based opening hook for cover letter.
        
        ENHANCED (2025-08-08): Now uses AI research engine for personalized content.
        """
        try:
            # Try to use enhanced AI research engine for personalized opening
            from ai_research_engine import AIResearchEngine
            
            research_engine = AIResearchEngine()
            
            # Prepare context for AI generation
            context = {
                'company_name': company_name,
                'recent_news': research_data.get('recent_news_analysis', '') if research_data else '',
                'role_title': research_data.get('role_title', 'Product Manager') if research_data else 'Product Manager'
            }
            
            # Generate AI-powered opening
            opening_result = research_engine.generate_personalized_content('cover_letter_opening', context)
            
            if opening_result.confidence > 0.5:
                logger.info(f"Generated AI-powered cover letter opening (confidence: {opening_result.confidence})")
                return opening_result.content
            else:
                logger.warning(f"AI-generated opening has low confidence ({opening_result.confidence}), using fallback")
                
        except Exception as e:
            logger.error(f"Error generating AI-powered opening: {e}")
        
        # Enhanced fallback logic using research data
        if research_data and "recent_news_analysis" in research_data:
            news_content = research_data['recent_news_analysis']
            # Extract a key development from the news (first 100 chars for brevity)
            key_development = news_content[:100].strip() + "..." if len(news_content) > 100 else news_content
            return f"I was excited to learn about {company_name}'s recent developments, particularly {key_development} - this aligns perfectly with my experience in scaling products through systematic experimentation and AI implementation."
        elif research_data and "recent_news" in research_data:
            return f"I was excited to see {company_name}'s recent {research_data.get('recent_news', 'developments')} - it aligns perfectly with my experience in scaling products through systematic experimentation and AI implementation."
        
        # Final fallback - generic but professional opening
        return f"I'm writing to express my interest in joining {company_name}'s product team, where I can apply my experience in growth strategy and product development to help drive your mission forward."
    
    def _generate_value_propositions(self, role_title: str, job_analysis: Dict) -> List[str]:
        """Generate 3-4 compelling value proposition points."""
        props = []
        
        # Role-specific value propositions
        if "growth" in role_title.lower():
            props.append("Proven track record of doubling conversion rates and scaling user acquisition through systematic experimentation")
            props.append("Experience implementing AI-powered growth strategies that shortened traditional processes from weeks to days")
        
        props.append("Unique combination of technical implementation skills and strategic thinking, with experience managing cross-functional teams")
        props.append("Deep expertise in user research and data-driven decision making, with measurable outcomes across B2B and B2C contexts")
        
        return props[:4]  # Limit to 4 maximum
    
    def _select_cover_letter_examples(self, role_title: str, job_analysis: Dict) -> List[str]:
        """Select 2-3 specific examples for cover letter."""
        examples = [
            "At Form Health, I doubled the freemium-to-premium conversion rate from 3.8% to 8.4% by redesigning the onboarding funnel and implementing systematic A/B testing",
            "Led the HP AI Companion launch from market research to product delivery in just 30 days by connecting user needs with technical capabilities",
            "Drove a 46% increase in enterprise sales leads at Vestis through systematic experimentation and stakeholder alignment"
        ]
        
        # Select most relevant examples based on role
        if "growth" in role_title.lower():
            return examples[:2]  # Focus on growth examples
        else:
            return [examples[1], examples[2]]  # Focus on product/strategy examples
    
    def _generate_call_to_action(self, company_name: str, role_title: str) -> str:
        """Generate specific call to action."""
        return f"I would welcome the opportunity to discuss how my experience in systematic product growth and AI implementation can contribute to {company_name}'s continued success. I'm excited to learn more about your product team's current priorities and how I can help drive meaningful impact in the {role_title} role."
    
    def _assemble_cover_letter(self, opening_hook: str, value_props: List[str], 
                              examples: List[str], call_to_action: str) -> str:
        """Assemble complete cover letter text."""
        # Format value propositions as bullet points
        props_text = "\n".join([f"• {prop}" for prop in value_props])
        
        # Format examples as paragraphs
        examples_text = "\n\n".join(examples)
        
        cover_letter = f"""{opening_hook}

I believe I can bring significant value to your team through:

{props_text}

Two examples that demonstrate this experience:

{examples_text}

{call_to_action}

Best regards,
Sam Zoloth"""
        
        return cover_letter
    
    def _generate_optimization_summary(self, company_name: str, role_title: str, 
                                     job_analysis: Dict) -> Dict:
        """Generate optimization summary for the application package."""
        return {
            "company_name": company_name,
            "role_title": role_title,
            "keywords_identified": job_analysis.get("keyword_count", 0),
            "optimization_focus": self._determine_optimization_focus(role_title),
            "personalization_elements": self._identify_personalization_elements(company_name),
            "recommendations": [
                "Review job analysis keywords and ensure resume incorporates key terms naturally",
                "Customize cover letter opening with specific company research insights",
                "Select case stories that best demonstrate relevant experience for this role",
                "Practice articulating quantified outcomes from selected examples"
            ]
        }
    
    def _determine_optimization_focus(self, role_title: str) -> str:
        """Determine primary optimization focus based on role."""
        if "growth" in role_title.lower():
            return "Growth metrics, conversion optimization, and user acquisition"
        elif "senior" in role_title.lower() or "principal" in role_title.lower():
            return "Leadership experience, strategic thinking, and cross-functional collaboration"
        elif "strategy" in role_title.lower():
            return "Strategic planning, competitive analysis, and roadmap development"
        else:
            return "Product management fundamentals and execution capabilities"
    
    def _identify_personalization_elements(self, company_name: str) -> List[str]:
        """Identify key personalization elements for this company."""
        return [
            f"Company-specific mission and values alignment",
            f"Recent news and developments at {company_name}",
            f"Product portfolio and competitive positioning insights",
            f"Growth challenges and opportunities specific to {company_name}"
        ]
    
    def _save_application_package(self, package: Dict) -> Path:
        """Save complete application package to company folder."""
        company_name = package["company_name"]
        company_key = company_name.lower().replace(" ", "_")
        company_dir = self.output_dir / company_key
        company_dir.mkdir(parents=True, exist_ok=True)
        
        # Save resume
        resume_filename = f"Sam_Zoloth_{company_name.replace(' ', '_')}_Resume.md"
        self._save_resume_markdown(package["resume"], company_dir / resume_filename)
        
        # Save cover letter
        cover_letter_filename = f"{company_name.replace(' ', '_')}_Cover_Letter.md"
        self._save_cover_letter_markdown(package["cover_letter"], company_dir / cover_letter_filename)
        
        # Save case stories
        case_stories_filename = f"Relevant_Case_Stories_{company_name.replace(' ', '_')}.md"
        self._save_case_stories_markdown(package["case_stories"], company_dir / case_stories_filename)
        
        # Save optimization report
        optimization_filename = f"Application_Optimization_Report.json"
        with open(company_dir / optimization_filename, 'w') as f:
            json.dump(package["optimization_summary"], f, indent=2)
        
        logger.info(f"Application package saved to: {company_dir}")
        return company_dir
    
    def _save_resume_markdown(self, resume: Dict, filepath: Path):
        """Save resume in markdown format."""
        header = resume["header"]
        
        content = f"""# {header["name"]}

**Email:** {header["email"]} | **Phone:** {header["phone"]}  
**LinkedIn:** {header["linkedin"]}

## Professional Summary

{resume["summary"]}

## Experience

"""
        
        for exp in resume["experience"]:
            content += f"""### {exp["title"]}
**{exp["company"]}** | {exp["location"]} | {exp["dates"]}

"""
            for bullet in exp["bullets"]:
                content += f"• {bullet}\n"
            content += "\n"
        
        content += "## Skills\n\n"
        for category, skills in resume["skills"].items():
            content += f"**{category}:** {', '.join(skills)}\n"
        
        with open(filepath, 'w') as f:
            f.write(content)
    
    def _save_cover_letter_markdown(self, cover_letter: Dict, filepath: Path):
        """Save cover letter in markdown format."""
        content = f"""# Cover Letter - {cover_letter["company_name"]}

**Role:** {cover_letter["role_title"]}  
**Date:** {datetime.now().strftime('%B %d, %Y')}

---

## Cover Letter Text

{cover_letter["full_text"]}

---

## Cover Letter Components

### Opening Hook
{cover_letter["opening_hook"]}

### Value Propositions
"""
        for prop in cover_letter["value_propositions"]:
            content += f"• {prop}\n"
        
        content += "\n### Examples\n"
        for example in cover_letter["examples"]:
            content += f"• {example}\n"
        
        content += f"\n### Call to Action\n{cover_letter['call_to_action']}"
        
        with open(filepath, 'w') as f:
            f.write(content)
    
    def _save_case_stories_markdown(self, case_stories: List[Dict], filepath: Path):
        """Save selected case stories in markdown format."""
        content = "# Relevant Case Stories\n\n"
        content += f"Selected case stories most relevant for this application.\n\n"
        
        for i, story in enumerate(case_stories, 1):
            content += f"""## {i}. {story.get("title", "Case Story")}

**Situation:** {story.get("situation", "")}

**Task:** {story.get("task", "")}

**Action:** {story.get("action", "")}

**Results:** {story.get("results", "")}

**Skills Demonstrated:** {", ".join(story.get("skills", []))}

---

"""
        
        with open(filepath, 'w') as f:
            f.write(content)

# Example usage
if __name__ == "__main__":
    generator = ApplicationGenerator()
    
    # Example application package generation
    package = generator.generate_application_package(
        company_name="Canva",
        role_title="Senior Product Manager",
        job_description="We are seeking a Senior Product Manager to drive growth...",
        research_data={"recent_news": "AI-powered design features launch"}
    )
    
    print(f"✅ Application package generated for {package['company_name']}")
    print(f"📊 Optimization Score: {package['optimization_summary']}")