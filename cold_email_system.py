#!/usr/bin/env python3
"""
Cold Email Campaign System

Automated cold email generation and management system implementing Sam's proven
direct outreach methodology. Bypasses online applications entirely through
targeted LinkedIn outreach and personalized email campaigns.

This system implements the "Never Apply Online" strategy:
- LinkedIn prospect identification and research
- Personalized cold email generation using proven templates
- Email sequence automation with strategic follow-ups
- Response tracking and pipeline management
- Network connection strategy optimization

Key Success Metrics:
- 40%+ response rate (vs. 2-5% for online applications)
- Zero automated rejections when going direct
- Higher conversion from first contact to interview

Usage:
    from cold_email_system import ColdEmailSystem
    
    email_system = ColdEmailSystem()
    campaign = email_system.create_email_campaign("Canva", "Senior Product Manager")
"""

import json
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class ColdEmailSystem:
    """
    Cold email campaign system implementing Sam's direct outreach methodology.
    
    Phase 4: Direct Outreach (NOT Online Applications)
    
    Core Components:
    1. LinkedIn prospect identification and research
    2. Decision maker targeting (CEO, Head of Product, Hiring Manager)
    3. Email address discovery and validation
    4. Personalized email generation using proven templates
    5. Follow-up sequence automation
    6. Response tracking and pipeline management
    
    Success Principles:
    - Never apply online - bypass the resume pile entirely
    - Target 1st/2nd degree hiring managers on LinkedIn
    - Use plain language, not buzzwords or corporate speak
    - Keep emails under 200 words with clear ask
    - Maximum one follow-up after 1 week
    """
    
    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.email_templates = self._load_email_templates()
        self.prospect_database = {}
        self.campaign_history = []
        self.output_dir = Path("Applications")
        
        # Email best practices from proven methodology
        self.email_rules = {
            "max_words": 200,
            "follow_up_days": 7,
            "max_follow_ups": 1,
            "personalization_required": True,
            "clear_ask_required": True
        }
    
    def create_email_campaign(self, company_name: str, role_title: str = None,
                            research_data: Dict = None, target_contacts: List[Dict] = None) -> Dict:
        """
        Create comprehensive cold email campaign for a company.
        
        Args:
            company_name: Target company name
            role_title: Target role (optional, used for personalization)
            research_data: Company research findings
            target_contacts: Specific contacts to target (optional)
            
        Returns:
            Complete email campaign package with personalized emails
        """
        logger.info(f"Creating cold email campaign for {company_name}")
        
        # Identify target contacts if not provided
        if not target_contacts:
            target_contacts = self._identify_target_contacts(company_name, role_title)
        
        # Generate personalized emails for each contact
        email_campaigns = []
        for contact in target_contacts:
            email_data = self._generate_personalized_email(
                contact, company_name, role_title, research_data
            )
            email_campaigns.append(email_data)
        
        # Create campaign package
        campaign = {
            "company_name": company_name,
            "role_title": role_title,
            "campaign_date": datetime.now().isoformat(),
            "target_contacts": target_contacts,
            "email_campaigns": email_campaigns,
            "follow_up_schedule": self._generate_follow_up_schedule(email_campaigns),
            "success_metrics": self._initialize_campaign_metrics(),
            "execution_guide": self._generate_execution_guide(company_name, email_campaigns)
        }
        
        # Save campaign to company folder
        self._save_email_campaign(campaign)
        
        logger.info(f"Cold email campaign created for {company_name} with {len(email_campaigns)} emails")
        return campaign
    
    def _identify_target_contacts(self, company_name: str, role_title: str = None) -> List[Dict]:
        """
        Identify target contacts for cold email outreach.
        
        Targeting Strategy (in priority order):
        1. Direct hiring manager for the role
        2. Head of Product / VP Product
        3. CEO (for smaller companies)
        4. Director of Product / Group Product Manager
        5. 1st/2nd degree LinkedIn connections
        """
        # Define target titles based on company size and role
        target_titles = self._get_target_titles(company_name, role_title)
        
        # Generate prospect list (would integrate with LinkedIn API)
        prospects = [
            {
                "name": "Target Hiring Manager",
                "title": "Head of Product",
                "company": company_name,
                "linkedin_url": f"https://linkedin.com/in/target-profile",
                "email_pattern": "firstname@company.com",
                "connection_degree": "2nd",
                "mutual_connections": [],
                "priority": "high",
                "personalization_data": {
                    "recent_posts": "Recent product launch announcement",
                    "background": "5+ years in product leadership",
                    "interests": "AI-powered product development"
                }
            },
            {
                "name": "VP Product",
                "title": "VP Product",
                "company": company_name,
                "linkedin_url": f"https://linkedin.com/in/vp-product",
                "email_pattern": "firstname@company.com",
                "connection_degree": "3rd",
                "mutual_connections": ["John Smith", "Jane Doe"],
                "priority": "medium",
                "personalization_data": {
                    "recent_posts": "Hiring team expansion",
                    "background": "Former Google PM",
                    "interests": "Product-led growth"
                }
            }
        ]
        
        return prospects
    
    def _get_target_titles(self, company_name: str, role_title: str = None) -> List[str]:
        """Get target titles to search for based on company and role."""
        # Base targeting titles
        base_titles = [
            "Head of Product",
            "VP Product", 
            "Director of Product",
            "Group Product Manager",
            "Chief Product Officer"
        ]
        
        # Add CEO for smaller companies
        company_size = self._estimate_company_size(company_name)
        if company_size < 200:
            base_titles.insert(0, "CEO")
            base_titles.insert(1, "Founder")
        
        # Add role-specific titles
        if role_title and "growth" in role_title.lower():
            base_titles.insert(0, "Head of Growth")
            base_titles.insert(1, "VP Growth")
        
        return base_titles
    
    def _estimate_company_size(self, company_name: str) -> int:
        """Estimate company size for targeting strategy."""
        # This would integrate with company database or API
        # For now, return estimated size based on known companies
        size_estimates = {
            "canva": 5000,
            "figma": 800,
            "notion": 500,
            "linear": 100,
            "stripe": 3000
        }
        
        company_lower = company_name.lower()
        for company, size in size_estimates.items():
            if company in company_lower:
                return size
        
        # Default to medium size
        return 300
    
    def _generate_personalized_email(self, contact: Dict, company_name: str, 
                                   role_title: str, research_data: Dict = None) -> Dict:
        """
        Generate personalized cold email for specific contact.
        
        Email Structure (Ben Lang's proven format):
        - Who you are
        - Why you're reaching out  
        - Why they should care
        
        Personalization Elements:
        - Recent company news/achievements
        - Contact's recent posts or background
        - Specific value proposition for their challenges
        - Mutual connections (if applicable)
        """
        # Select appropriate email template
        template = self._select_email_template(contact, role_title)
        
        # Generate personalization elements
        personalization = self._generate_personalization(contact, company_name, research_data)
        
        # Create email content
        email_content = self._populate_email_template(
            template, contact, company_name, role_title, personalization
        )
        
        # Validate email against best practices
        validation_result = self._validate_email(email_content)
        
        email_data = {
            "contact": contact,
            "template_used": template["name"],
            "personalization": personalization,
            "email_content": email_content,
            "validation": validation_result,
            "send_priority": contact.get("priority", "medium"),
            "suggested_send_time": self._suggest_send_time(),
            "follow_up_sequence": self._generate_follow_up_sequence(contact, email_content),
            "success_probability": self._estimate_success_probability(contact, email_content)
        }
        
        return email_data
    
    def _load_email_templates(self) -> Dict[str, Dict]:
        """
        Load proven cold email templates.
        
        Templates based on successful examples:
        - Brian Kemler's high-response format
        - Ben Lang's cold email guide
        - Sam's proven outreach methodology
        """
        return {
            "product_manager_growth": {
                "name": "Product Manager - Growth Focus",
                "subject_line": "Growth expertise for {company_name}",
                "template": """Hi {name},

{personalization_hook}

I'm reaching out because {specific_reason}. Two things that might be relevant:

• {achievement_1}
• {achievement_2}

I think I could help you {specific_value_add} and would like to learn more about your current priorities.

Worth a 15-minute conversation?

Best,
Sam Zoloth""",
                "personalization_required": ["personalization_hook", "specific_reason", "achievement_1", "achievement_2", "specific_value_add"],
                "max_words": 200,
                "target_roles": ["product manager", "growth"]
            },
            
            "senior_leadership": {
                "name": "Senior Leadership Outreach", 
                "subject_line": "Product strategy expertise for {company_name}",
                "template": """Hi {name},

{personalization_hook}

I specialize in helping companies scale their product development through systematic experimentation and AI implementation. 

My experience includes:
• {relevant_experience_1}
• {relevant_experience_2}

I'm particularly interested in {company_challenge} and believe I could contribute to your team's success.

Would you have time for a brief conversation about your product priorities?

Best regards,
Sam Zoloth""",
                "personalization_required": ["personalization_hook", "relevant_experience_1", "relevant_experience_2", "company_challenge"],
                "max_words": 180,
                "target_roles": ["director", "vp", "head", "ceo"]
            },
            
            "ai_focused": {
                "name": "AI/Technology Focus",
                "subject_line": "AI product expertise for {company_name}",
                "template": """Hi {name},

{personalization_hook}

I saw {company_name} is {ai_initiative} and wanted to reach out. I recently helped HP launch their AI Companion from research to market in 30 days, and have experience scaling AI-powered products.

Two relevant outcomes:
• {ai_achievement_1}  
• {ai_achievement_2}

Happy to share more about how systematic AI implementation could accelerate {company_name}'s product roadmap.

Interested in a quick chat?

Sam""",
                "personalization_required": ["personalization_hook", "ai_initiative", "ai_achievement_1", "ai_achievement_2"],
                "max_words": 150,
                "target_roles": ["ai", "ml", "technology", "innovation"]
            }
        }
    
    def _select_email_template(self, contact: Dict, role_title: str = None) -> Dict:
        """Select most appropriate email template for contact and role."""
        contact_title = contact.get("title", "").lower()
        
        # AI/ML focus for tech-forward companies
        if any(term in contact_title for term in ["ai", "ml", "data", "technology"]):
            return self.email_templates["ai_focused"]
        
        # Senior leadership template for executives
        if any(term in contact_title for term in ["ceo", "vp", "head", "chief", "director"]):
            return self.email_templates["senior_leadership"]
        
        # Growth focus for growth-related roles
        if role_title and "growth" in role_title.lower():
            return self.email_templates["product_manager_growth"]
        
        # Default to product manager template
        return self.email_templates["product_manager_growth"]
    
    def _generate_personalization(self, contact: Dict, company_name: str, 
                                research_data: Dict = None) -> Dict:
        """
        Generate personalization elements for email.
        
        ENHANCED (2025-08-08): Now uses AI research engine for better personalization.
        
        Personalization Sources:
        - Recent company news/developments (now AI-generated)
        - Contact's LinkedIn activity
        - Company research findings (now enhanced with AI)
        - Mutual connections
        - Industry trends
        """
        personalization_data = contact.get("personalization_data", {})
        
        # Try to use AI research engine for enhanced personalization
        try:
            from ai_research_engine import AIResearchEngine
            
            research_engine = AIResearchEngine()
            
            # Prepare context for AI personalization
            context = {
                'company_name': company_name,
                'contact_info': contact,
                'recent_developments': research_data.get('recent_news_analysis', '') if research_data else ''
            }
            
            # Generate AI-powered personalization
            personalization_result = research_engine.generate_personalized_content('cold_email_personalization', context)
            
            if personalization_result.confidence > 0.5:
                # Parse AI-generated personalization
                ai_content = personalization_result.content
                
                # Extract components from AI response (simple parsing)
                lines = [line.strip() for line in ai_content.split('\n') if line.strip()]
                
                # Try to extract structured elements
                personalization_hook = lines[0] if lines else f"I've been following {company_name}'s growth"
                specific_reason = lines[1] if len(lines) > 1 else f"your team's focus on innovation aligns with my experience"
                company_challenge = lines[2] if len(lines) > 2 else "scaling product development"
                
                logger.info(f"Generated AI-powered email personalization (confidence: {personalization_result.confidence})")
                
                # Clean up the content
                if personalization_hook.startswith('1.'):
                    personalization_hook = personalization_hook[3:].strip()
                if specific_reason.startswith('2.'):
                    specific_reason = specific_reason[3:].strip()
                if company_challenge.startswith('3.'):
                    company_challenge = company_challenge[3:].strip()
                    
            else:
                logger.warning(f"AI personalization has low confidence, using fallback")
                raise Exception("Low confidence AI result")
                
        except Exception as e:
            logger.error(f"Error generating AI personalization: {e}")
            
            # Fallback to enhanced manual logic
            hooks = []
            
            # Enhanced company news hook using AI-generated research
            if research_data and "recent_news_analysis" in research_data:
                news_content = research_data['recent_news_analysis']
                # Extract key theme from news (simple approach)
                key_theme = news_content[:50].strip() + "..." if len(news_content) > 50 else news_content
                hooks.append(f"I saw {company_name}'s recent developments, particularly {key_theme}")
            elif research_data and "recent_news" in research_data:
                hooks.append(f"I saw {company_name}'s recent {research_data['recent_news']} - impressive progress on {research_data.get('focus_area', 'product development')}")
            
            # Contact background hook  
            if personalization_data.get("recent_posts"):
                hooks.append(f"I noticed your recent post about {personalization_data['recent_posts']}")
            
            # Industry/competitive hook
            hooks.append(f"I've been following {company_name}'s growth in the {research_data.get('industry', 'tech')} space")
            
            # Select best hook
            personalization_hook = hooks[0] if hooks else f"I've been following {company_name}'s product development"
            specific_reason = f"your team's focus on product innovation aligns with my experience in systematic product development"
            company_challenge = research_data.get('key_challenges', 'scaling product development') if research_data else 'product growth challenges'
        
        # Generate specific reason for reaching out
        reasons = [
            f"you're expanding the product team and I think I could help accelerate your growth initiatives",
            f"I have experience with similar challenges in scaling product development at high-growth companies",
            f"my background in systematic experimentation could support {company_name}'s current priorities"
        ]
        
        specific_reason = reasons[0]
        
        # Generate achievements
        achievements = self._select_relevant_achievements(contact, research_data)
        
        # Generate specific value add
        value_adds = [
            f"scale your product development through systematic experimentation",
            f"implement AI-powered solutions to accelerate product roadmap", 
            f"optimize growth metrics through data-driven product improvements"
        ]
        
        return {
            "personalization_hook": personalization_hook,
            "specific_reason": specific_reason,
            "achievement_1": achievements[0],
            "achievement_2": achievements[1], 
            "specific_value_add": value_adds[0],
            "relevant_experience_1": achievements[0],
            "relevant_experience_2": achievements[1],
            "company_challenge": research_data.get("key_challenges", "product growth challenges") if research_data else "scaling product development",
            "ai_initiative": research_data.get("ai_initiatives", "implementing AI-powered features") if research_data else "exploring AI capabilities",
            "ai_achievement_1": "HP AI Companion launch from research to market in 30 days",
            "ai_achievement_2": "Systematic experimentation that doubled conversion rates at Form Health"
        }
    
    def _select_relevant_achievements(self, contact: Dict, research_data: Dict = None) -> List[str]:
        """Select most relevant achievements for the contact and company."""
        all_achievements = [
            "Doubled freemium-to-premium conversion rate from 3.8% to 8.4% through systematic A/B testing",
            "Launched HP AI Companion from market research to delivery in 30 days",
            "Grew organic traffic from <100 to 10K monthly visitors in 4 months through systematic SEO",
            "Drove 46% increase in enterprise sales leads through experimentation program",
            "Led end-to-end product redesign with 65% Customer Effort Score improvement",
            "Enabled $13M+ in new business through AI-driven research and growth models",
            "Increased free trial conversion rate from 2.7% to 4.4% (+63%) for B2B SaaS company"
        ]
        
        contact_title = contact.get("title", "").lower()
        
        # Prioritize achievements based on contact role
        if "growth" in contact_title:
            # Prioritize conversion and growth achievements
            prioritized = [a for a in all_achievements if any(term in a.lower() for term in ["conversion", "growth", "traffic", "leads"])]
        elif "ai" in contact_title or "technology" in contact_title:
            # Prioritize AI and technical achievements
            prioritized = [a for a in all_achievements if any(term in a.lower() for term in ["ai", "systematic", "research"])]
        else:
            # General product achievements
            prioritized = all_achievements
        
        # Ensure we have at least 2 achievements
        if len(prioritized) < 2:
            prioritized = all_achievements
        
        return prioritized[:2]
    
    def _populate_email_template(self, template: Dict, contact: Dict, 
                               company_name: str, role_title: str, 
                               personalization: Dict) -> Dict:
        """Populate email template with personalized content."""
        # Format subject line
        subject_line = template["subject_line"].format(
            company_name=company_name,
            name=contact.get("name", "")
        )
        
        # Format email body
        email_body = template["template"].format(
            name=contact.get("name", "there"),
            company_name=company_name,
            **personalization
        )
        
        # Calculate word count
        word_count = len(email_body.split())
        
        return {
            "subject_line": subject_line,
            "body": email_body,
            "word_count": word_count,
            "template_name": template["name"]
        }
    
    def _validate_email(self, email_content: Dict) -> Dict:
        """
        Validate email against proven best practices.
        
        Validation Rules (Ben Lang's Guidelines):
        - Under 200 words
        - No fancy words/buzzwords
        - Clear ask included
        - Specific and not vague
        - Honest and not spammy
        """
        validation_results = {
            "passed": True,
            "warnings": [],
            "suggestions": []
        }
        
        body = email_content["body"]
        word_count = email_content["word_count"]
        
        # Word count check
        if word_count > 200:
            validation_results["warnings"].append(f"Email is {word_count} words (should be under 200)")
            validation_results["passed"] = False
        
        # Clear ask check
        ask_indicators = ["conversation", "chat", "meeting", "call", "discuss", "worth", "interested"]
        has_ask = any(indicator in body.lower() for indicator in ask_indicators)
        if not has_ask:
            validation_results["warnings"].append("No clear ask detected in email")
            validation_results["passed"] = False
        
        # Buzzword check
        buzzwords = ["synergy", "leverage", "optimize", "execute", "drive results", "best practices"]
        found_buzzwords = [word for word in buzzwords if word in body.lower()]
        if found_buzzwords:
            validation_results["warnings"].append(f"Buzzwords detected: {', '.join(found_buzzwords)}")
            validation_results["suggestions"].append("Replace buzzwords with plain language")
        
        # Specificity check
        vague_phrases = ["results", "impact", "value", "solutions"]
        vague_count = sum(1 for phrase in vague_phrases if phrase in body.lower())
        if vague_count > 2:
            validation_results["suggestions"].append("Add more specific examples and metrics")
        
        return validation_results
    
    def _suggest_send_time(self) -> Dict:
        """Suggest optimal send time for cold emails."""
        return {
            "day": "Tuesday-Thursday",
            "time": "9:00-11:00 AM or 2:00-4:00 PM",
            "timezone": "Recipient's local timezone", 
            "reasoning": "Higher open rates during business hours mid-week"
        }
    
    def _generate_follow_up_sequence(self, contact: Dict, initial_email: Dict) -> List[Dict]:
        """
        Generate follow-up email sequence.
        
        Follow-up Strategy:
        - Wait 7 days after initial email
        - Send only ONE follow-up maximum
        - Brief and polite reminder
        - Add additional value or insight
        """
        follow_up = {
            "delay_days": 7,
            "subject_line": f"Re: {initial_email['subject_line']}",
            "body": f"""Hi {contact.get('name', 'there')},

I wanted to follow up on my previous email about product growth opportunities at {contact.get('company')}.

I understand you're likely busy, but if you have 15 minutes in the coming weeks, I'd love to share some insights from recent AI product launches that might be relevant to your team's roadmap.

No worries if the timing isn't right.

Best,
Sam""",
            "max_follow_ups": 1,
            "send_only_if_no_response": True
        }
        
        return [follow_up]
    
    def _estimate_success_probability(self, contact: Dict, email_content: Dict) -> float:
        """Estimate probability of positive response based on contact and email quality."""
        base_probability = 0.4  # 40% base success rate for direct outreach
        
        # Adjust based on connection degree
        connection_degree = contact.get("connection_degree", "3rd")
        if connection_degree == "1st":
            base_probability += 0.3  # 70% for direct connections
        elif connection_degree == "2nd":
            base_probability += 0.1  # 50% for 2nd degree
        
        # Adjust for mutual connections
        mutual_connections = contact.get("mutual_connections", [])
        if len(mutual_connections) > 0:
            base_probability += 0.1
        
        # Adjust for email quality
        validation = email_content.get("validation", {})
        if not validation.get("passed", True):
            base_probability -= 0.15
        
        # Adjust for contact priority
        if contact.get("priority") == "high":
            base_probability += 0.1
        
        return min(base_probability, 0.9)  # Cap at 90%
    
    def _generate_follow_up_schedule(self, email_campaigns: List[Dict]) -> Dict:
        """Generate follow-up schedule for all emails in campaign."""
        schedule = {
            "initial_send_dates": {},
            "follow_up_dates": {},
            "tracking_reminders": []
        }
        
        today = datetime.now()
        
        for i, campaign in enumerate(email_campaigns):
            contact_name = campaign["contact"]["name"]
            
            # Stagger initial sends
            send_date = today + timedelta(days=i)  # Send one per day
            schedule["initial_send_dates"][contact_name] = send_date.isoformat()
            
            # Schedule follow-up
            follow_up_date = send_date + timedelta(days=7)
            schedule["follow_up_dates"][contact_name] = follow_up_date.isoformat()
            
            # Tracking reminders
            schedule["tracking_reminders"].append({
                "contact": contact_name,
                "check_date": (send_date + timedelta(days=3)).isoformat(),
                "action": "Check for response and LinkedIn activity"
            })
        
        return schedule
    
    def _initialize_campaign_metrics(self) -> Dict:
        """Initialize success metrics tracking for campaign."""
        return {
            "emails_sent": 0,
            "responses_received": 0,
            "response_rate": 0.0,
            "meetings_scheduled": 0,
            "conversion_rate": 0.0,
            "follow_ups_sent": 0,
            "linkedin_connections": 0,
            "target_response_rate": 0.4  # 40% target
        }
    
    def _generate_execution_guide(self, company_name: str, email_campaigns: List[Dict]) -> Dict:
        """Generate execution guide for the email campaign."""
        return {
            "campaign_overview": f"{len(email_campaigns)} personalized emails for {company_name}",
            "execution_steps": [
                "1. Review and customize each email as needed",
                "2. Research contact email addresses using firstname@company.com pattern",
                "3. Send emails according to schedule (1 per day to avoid appearing spammy)",
                "4. Connect with contacts on LinkedIn after sending email",
                "5. Track responses and schedule follow-ups",
                "6. Update pipeline with outcomes"
            ],
            "email_discovery_tips": [
                "Try firstname@company.com format first",
                "Use tools like ContactOut, Apollo, or Nymeria for email discovery",
                "Check company about pages for email format patterns",
                "Leverage mutual connections for warm introductions when possible"
            ],
            "linkedin_strategy": [
                "Send LinkedIn connection request same day as email",
                "Use personalized connection message referencing your email",
                "Engage with their recent posts appropriately", 
                "Use LinkedIn to research additional context for follow-ups"
            ],
            "success_tracking": [
                "Track open rates if using email tracking tools",
                "Monitor LinkedIn profile views and connection acceptances",
                "Log all responses in pipeline tracking system",
                "Schedule follow-ups exactly 7 days after initial send"
            ]
        }
    
    def _save_email_campaign(self, campaign: Dict) -> Path:
        """Save email campaign to company folder."""
        company_name = campaign["company_name"]
        company_key = company_name.lower().replace(" ", "_")
        company_dir = self.output_dir / company_key
        company_dir.mkdir(parents=True, exist_ok=True)
        
        # Save comprehensive email campaign file
        campaign_file = company_dir / f"{company_name.replace(' ', '_')}_Cold_Email_Campaign.md"
        
        campaign_content = f"""# Cold Email Campaign - {company_name}

**Role:** {campaign.get('role_title', 'Product Management')}  
**Campaign Date:** {campaign['campaign_date']}  
**Target Contacts:** {len(campaign['email_campaigns'])}

---

## Campaign Overview

This campaign implements Sam's proven "Never Apply Online" methodology with personalized cold emails to hiring managers and product leaders.

**Target Response Rate:** 40%+ (vs. 2-5% for online applications)  
**Strategy:** Direct outreach to 1st/2nd degree connections  
**Follow-up Rule:** Maximum 1 follow-up after 7 days

---

## Email Campaigns

{self._format_email_campaigns(campaign['email_campaigns'])}

---

## Execution Schedule

{self._format_execution_schedule(campaign['follow_up_schedule'])}

---

## Execution Guide

{self._format_execution_guide(campaign['execution_guide'])}

---

## Success Tracking

{self._format_success_metrics(campaign['success_metrics'])}

Update this file with:
- [ ] Email send dates and responses
- [ ] LinkedIn connection outcomes  
- [ ] Meeting schedules and interview opportunities
- [ ] Response rate and conversion metrics
"""
        
        with open(campaign_file, 'w') as f:
            f.write(campaign_content)
        
        # Save individual email files for easy copy/paste
        emails_dir = company_dir / "cold_emails"
        emails_dir.mkdir(exist_ok=True)
        
        for i, email_campaign in enumerate(campaign['email_campaigns'], 1):
            contact = email_campaign['contact']
            email_file = emails_dir / f"{i:02d}_{contact['name'].replace(' ', '_').lower()}.md"
            
            with open(email_file, 'w') as f:
                f.write(f"""# Cold Email - {contact['name']}

**Company:** {contact['company']}  
**Title:** {contact['title']}  
**Priority:** {contact['priority']}  
**LinkedIn:** {contact.get('linkedin_url', 'N/A')}  
**Estimated Success Rate:** {email_campaign['success_probability']:.1%}

---

## Email Content

**Subject:** {email_campaign['email_content']['subject_line']}

**Body:**
```
{email_campaign['email_content']['body']}
```

**Word Count:** {email_campaign['email_content']['word_count']}/200

---

## Personalization Elements

{self._format_personalization(email_campaign['personalization'])}

---

## Follow-up Sequence

{self._format_follow_up_sequence(email_campaign['follow_up_sequence'])}

---

## Email Discovery

**Suggested Email:** {contact['email_pattern']}  
**Connection Degree:** {contact['connection_degree']}  
**Mutual Connections:** {', '.join(contact.get('mutual_connections', ['None']))}

---

## Tracking

- [ ] Email sent on: ___________
- [ ] LinkedIn connection sent: ___________
- [ ] Response received: ___________
- [ ] Follow-up sent (if needed): ___________  
- [ ] Meeting scheduled: ___________
""")
        
        logger.info(f"Email campaign saved to: {campaign_file}")
        return campaign_file
    
    def _format_email_campaigns(self, campaigns: List[Dict]) -> str:
        """Format email campaigns for markdown display."""
        formatted = ""
        
        for i, campaign in enumerate(campaigns, 1):
            contact = campaign['contact']
            email = campaign['email_content']
            
            formatted += f"""### {i}. {contact['name']} - {contact['title']}

**Priority:** {contact['priority']} | **Success Rate:** {campaign['success_probability']:.1%}  
**LinkedIn:** {contact.get('linkedin_url', 'N/A')}

**Subject:** {email['subject_line']}

**Email Preview:**
```
{email['body'][:200]}{'...' if len(email['body']) > 200 else ''}
```

**Validation:** {'✅ Passed' if campaign['validation']['passed'] else '⚠️ Needs Review'}  
**Word Count:** {email['word_count']}/200

---

"""
        
        return formatted
    
    def _format_execution_schedule(self, schedule: Dict) -> str:
        """Format execution schedule for markdown display."""
        formatted = "### Send Schedule\n\n"
        
        for contact, date in schedule['initial_send_dates'].items():
            send_date = datetime.fromisoformat(date).strftime('%B %d, %Y')
            formatted += f"- **{contact}:** {send_date}\n"
        
        formatted += "\n### Follow-up Schedule\n\n"
        
        for contact, date in schedule['follow_up_dates'].items():
            follow_date = datetime.fromisoformat(date).strftime('%B %d, %Y')
            formatted += f"- **{contact}:** {follow_date} (if no response)\n"
        
        return formatted
    
    def _format_execution_guide(self, guide: Dict) -> str:
        """Format execution guide for markdown display."""
        formatted = f"**{guide['campaign_overview']}**\n\n"
        
        formatted += "### Execution Steps\n"
        for step in guide['execution_steps']:
            formatted += f"{step}\n"
        
        formatted += "\n### Email Discovery Tips\n"
        for tip in guide['email_discovery_tips']:
            formatted += f"- {tip}\n"
        
        formatted += "\n### LinkedIn Strategy\n" 
        for strategy in guide['linkedin_strategy']:
            formatted += f"- {strategy}\n"
        
        return formatted
    
    def _format_success_metrics(self, metrics: Dict) -> str:
        """Format success metrics for markdown display."""
        return f"""**Target Response Rate:** {metrics['target_response_rate']:.0%}

### Tracking Metrics
- Emails Sent: {metrics['emails_sent']}/{metrics.get('total_planned', 'TBD')}
- Responses Received: {metrics['responses_received']}
- Response Rate: {metrics['response_rate']:.1%}
- Meetings Scheduled: {metrics['meetings_scheduled']}
- LinkedIn Connections: {metrics['linkedin_connections']}"""
    
    def _format_personalization(self, personalization: Dict) -> str:
        """Format personalization elements for display."""
        formatted = ""
        for key, value in personalization.items():
            formatted += f"- **{key.replace('_', ' ').title()}:** {value}\n"
        return formatted
    
    def _format_follow_up_sequence(self, sequence: List[Dict]) -> str:
        """Format follow-up sequence for display."""
        if not sequence:
            return "No follow-up planned"
        
        follow_up = sequence[0]
        return f"""**Delay:** {follow_up['delay_days']} days after initial email  
**Subject:** {follow_up['subject_line']}  
**Body:**
```
{follow_up['body']}
```"""

# Example usage
if __name__ == "__main__":
    email_system = ColdEmailSystem()
    
    # Example campaign creation
    campaign = email_system.create_email_campaign(
        company_name="Canva",
        role_title="Senior Product Manager",
        research_data={
            "recent_news": "AI-powered design features launch",
            "key_challenges": "scaling AI adoption",
            "industry": "design and creative tools"
        }
    )
    
    print(f"✅ Cold email campaign created for {campaign['company_name']}")
    print(f"📧 {len(campaign['email_campaigns'])} personalized emails generated")
    print(f"🎯 Target response rate: {campaign['success_metrics']['target_response_rate']:.0%}")