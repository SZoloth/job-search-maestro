#!/usr/bin/env python3
"""
Job Search Orchestrator - Master Command Center

A bulletproof automation framework for Sam Zoloth's job search process,
implementing the Never Search Alone methodology with AI-powered research,
systematic application generation, and cold email campaigns.

This script orchestrates the entire job search workflow:
1. Company research and qualification
2. Application package generation (resume, cover letter, case stories)
3. Cold email campaign management
4. Interview preparation automation
5. Progress tracking and follow-up management

Usage:
    python job_search_orchestrator.py [command] [options]

Commands:
    research    - Research a company and assess fit
    apply       - Generate application package for a company
    email       - Create and send cold email campaign
    prep        - Generate interview preparation materials
    track       - View pipeline status and next actions
    config      - Configure settings and templates
"""

import json
import os
import sys
import argparse
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('job_search.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class JobSearchOrchestrator:
    """
    Master orchestrator for the entire job search process.
    
    Implements Sam's proven methodology:
    - Never Search Alone principles
    - AI-powered research and preparation
    - Systematic application generation
    - Cold email campaigns with high response rates
    - Interview preparation automation
    """
    
    def __init__(self):
        self.base_path = Path(__file__).parent
        self.config_file = self.base_path / "config" / "job_search_config.json"
        self.pipeline_file = self.base_path / "data" / "application_pipeline.json"
        self.templates_dir = self.base_path / "templates"
        self.output_dir = self.base_path / "Applications"
        
        # Ensure directories exist
        for dir_path in [self.config_file.parent, self.pipeline_file.parent, 
                        self.templates_dir, self.output_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
        
        self.config = self.load_config()
        self.pipeline = self.load_pipeline()
        
        # Import automation modules
        self.research_engine = None
        self.package_generator = None
        self.email_system = None
        self.interview_prep = None
        
    def load_config(self) -> Dict:
        """Load configuration settings."""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                return json.load(f)
        
        # Default configuration
        default_config = {
            "user_profile": {
                "name": "Sam Zoloth",
                "email": "zoloth@hey.com", 
                "phone": "617-943-0717",
                "linkedin": "linkedin.com/in/samuelzoloth/",
                "target_roles": [
                    "Senior Product Manager",
                    "Growth Product Manager", 
                    "Principal Product Manager",
                    "Director of Product"
                ],
                "target_industries": [
                    "Healthcare Technology",
                    "Consumer Products",
                    "AI/ML Companies",
                    "EdTech",
                    "FinTech"
                ],
                "target_company_size": "50-500 employees",
                "remote_preference": "Fully remote or flexible hybrid",
                "salary_range": "$150-180K base"
            },
            "ai_prompts": {
                "company_research": """Create a comprehensive company dossier for {company_name} for a {target_role} preparing for interviews. Include: mission/values, founders, products, competitors, recent news. Focus on trust, safety, privacy, regulatory, or AI-related news. Cover business model and key challenges.""",
                "industry_research": """You're a director of PM for {specific_team} at a company like {company_name}. Research how to {solve_key_problem}. Write a comprehensive brief on problems (with metrics) and survey what the industry has done to improve {specific_area}."""
            },
            "email_settings": {
                "max_words": 200,
                "follow_up_days": 7,
                "max_follow_ups": 1
            },
            "quality_gates": {
                "min_priority_score": 28,
                "required_research_time": 45,
                "application_time_budget": 180
            }
        }
        
        # Save default config
        with open(self.config_file, 'w') as f:
            json.dump(default_config, f, indent=2)
            
        return default_config
    
    def load_pipeline(self) -> Dict:
        """Load application pipeline data."""
        if self.pipeline_file.exists():
            with open(self.pipeline_file, 'r') as f:
                return json.load(f)
        
        # Default pipeline structure
        default_pipeline = {
            "companies": {},
            "stats": {
                "total_researched": 0,
                "total_applied": 0,
                "response_rate": 0.0,
                "interviews_scheduled": 0,
                "offers_received": 0
            },
            "next_actions": []
        }
        
        return default_pipeline
    
    def save_pipeline(self):
        """Save pipeline data to file."""
        with open(self.pipeline_file, 'w') as f:
            json.dump(self.pipeline, f, indent=2)
    
    def _update_pipeline_status(self, company_name: str, field: str, value):
        """Update specific field in pipeline for a company."""
        company_key = company_name.lower()
        if company_key in self.pipeline['companies']:
            self.pipeline['companies'][company_key][field] = value
            # Update status based on progress
            if field == 'application_generated' and value:
                self.pipeline['companies'][company_key]['status'] = 'applied'
            elif field == 'emails_sent' and value:
                self.pipeline['companies'][company_key]['status'] = 'outreach_sent'
            self.save_pipeline()
    
    def _load_company_data(self, company_name: str) -> Dict:
        """Load existing research data for a company."""
        company_key = company_name.lower()
        return self.pipeline['companies'].get(company_key, {})
    
    def research_company(self, company_name: str, role_title: str = None, 
                        force_refresh: bool = False, scores: Dict = None) -> Dict:
        """
        Phase 2: Deep Research (45-60 minutes automated)
        
        Conducts comprehensive company research including:
        - AI-powered company intelligence
        - Role & team research
        - Network activation opportunities
        - Priority scoring and qualification
        """
        logger.info(f"Researching company: {company_name}")
        
        # Check if already researched
        company_key = company_name.lower().replace(" ", "_")
        if not force_refresh and company_key in self.pipeline["companies"]:
            existing = self.pipeline["companies"][company_key]
            if existing.get("research_completed"):
                logger.info(f"Company {company_name} already researched. Use --force-refresh to update.")
                return existing
        
        # Initialize company record
        company_data = {
            "name": company_name,
            "research_date": datetime.now().isoformat(),
            "role_title": role_title,
            "priority_score": 0,
            "qualification_passed": False,
            "research_completed": False,
            "application_generated": False,
            "emails_sent": [],
            "interviews": [],
            "status": "researching"
        }
        
        print(f"\n🔍 PHASE 2: DEEP RESEARCH - {company_name}")
        print("=" * 60)
        
        # Quick qualification check (Phase 1)
        print("\n📋 Quick Qualification Check:")
        if scores:
            priority_scores = {
                "role_appeal": scores.get("role_appeal", 8),
                "company_fit": scores.get("company_fit", 8), 
                "growth_potential": scores.get("growth_potential", 8),
                "likelihood": scores.get("likelihood", 8)
            }
            total = sum(priority_scores.values())
            print(f"📊 Using provided scores - Total: {total}/40")
        else:
            priority_scores = self._quick_qualification_check(company_name, role_title)
        company_data["priority_score"] = sum(priority_scores.values())
        company_data["priority_breakdown"] = priority_scores
        
        if company_data["priority_score"] < self.config["quality_gates"]["min_priority_score"]:
            print(f"❌ Company scored {company_data['priority_score']}/40. Below threshold of {self.config['quality_gates']['min_priority_score']}.")
            print("⏭️  Skipping detailed research. Consider other opportunities.")
            company_data["status"] = "disqualified"
            self.pipeline["companies"][company_key] = company_data
            self.save_pipeline()
            return company_data
        
        print(f"✅ Company scored {company_data['priority_score']}/40. Proceeding with deep research.")
        
        # AI-Powered Company Intelligence
        print("\n🤖 AI-Powered Company Intelligence:")
        research_data = self._conduct_ai_research(company_name, role_title)
        company_data.update(research_data)
        
        # Network activation analysis
        print("\n🔗 Network Activation Analysis:")
        network_data = self._analyze_network_opportunities(company_name)
        company_data["network_opportunities"] = network_data
        
        # Mark research as completed
        company_data["research_completed"] = True
        company_data["status"] = "researched"
        company_data["qualification_passed"] = True
        
        # Save to pipeline
        self.pipeline["companies"][company_key] = company_data
        self.pipeline["stats"]["total_researched"] += 1
        self.save_pipeline()
        
        # Generate research summary
        self._generate_research_summary(company_data)
        
        print(f"\n✅ Research completed for {company_name}")
        print(f"📁 Research files saved to: Applications/{company_key}/")
        print(f"📊 Priority Score: {company_data['priority_score']}/40")
        
        return company_data
    
    def _quick_qualification_check(self, company_name: str, role_title: str) -> Dict[str, int]:
        """
        Phase 1: Initial Assessment (15 minutes)
        
        Interactive qualification check with priority scoring:
        - Role Appeal (1-10)
        - Company Fit (1-10) 
        - Growth Potential (1-10)
        - Likelihood (1-10)
        """
        print(f"\nPlease rate {company_name} on a scale of 1-10:")
        
        scores = {}
        
        # Role Appeal
        while True:
            try:
                score = int(input("🎯 Role Appeal - How excited are you about this specific role? (1-10): "))
                if 1 <= score <= 10:
                    scores["role_appeal"] = score
                    break
                else:
                    print("Please enter a number between 1 and 10.")
            except ValueError:
                print("Please enter a valid number.")
        
        # Company Fit
        while True:
            try:
                score = int(input("🏢 Company Fit - How well does the company align with your values/goals? (1-10): "))
                if 1 <= score <= 10:
                    scores["company_fit"] = score
                    break
                else:
                    print("Please enter a number between 1 and 10.")
            except ValueError:
                print("Please enter a valid number.")
        
        # Growth Potential
        while True:
            try:
                score = int(input("📈 Growth Potential - What learning/advancement opportunities exist? (1-10): "))
                if 1 <= score <= 10:
                    scores["growth_potential"] = score
                    break
                else:
                    print("Please enter a number between 1 and 10.")
            except ValueError:
                print("Please enter a valid number.")
        
        # Likelihood
        while True:
            try:
                score = int(input("🎲 Likelihood - How competitive are you for this role? (1-10): "))
                if 1 <= score <= 10:
                    scores["likelihood"] = score
                    break
                else:
                    print("Please enter a number between 1 and 10.")
            except ValueError:
                print("Please enter a valid number.")
        
        total = sum(scores.values())
        print(f"\n📊 Priority Scoring Results:")
        for category, score in scores.items():
            print(f"  {category.replace('_', ' ').title()}: {score}/10")
        print(f"  Total Score: {total}/40")
        
        return scores
    
    def _conduct_ai_research(self, company_name: str, role_title: str) -> Dict:
        """
        Conduct AI-powered research using enhanced AI research engine.
        
        ENHANCED (2025-08-08): Now generates real AI content instead of placeholders.
        
        This integrates with the enhanced AI research engine:
        1. Company dossier creation with real AI generation
        2. Industry-specific deep research with actual insights
        3. Competitive analysis with real data
        4. Recent news analysis with current information
        """
        print("🤖 Generating AI-powered company intelligence...")
        
        try:
            # Import and use the enhanced AI research engine
            from ai_research_engine import AIResearchEngine
            
            # Initialize research engine
            research_engine = AIResearchEngine()
            
            print("⏳ Generating comprehensive company dossier...")
            print("⏳ Conducting industry-specific deep research...")
            print("⏳ Analyzing competitive landscape...")
            print("⏳ Researching recent news and developments...")
            
            # Generate real AI research
            ai_research_results = research_engine.generate_company_intelligence(company_name, role_title)
            
            # Convert to original format for backward compatibility
            research_data = {}
            for research_type, result in ai_research_results.items():
                research_data[research_type] = result.content
                print(f"✅ Generated {research_type.replace('_', ' ').title()}: {len(result.content)} characters (confidence: {result.confidence:.1f})")
            
            # Add legacy field mappings for backward compatibility
            if 'company_dossier' in research_data:
                research_data['business_model'] = "See company dossier for business model details"
                research_data['key_challenges'] = "See company dossier and competitive analysis for key challenges"
            
            if 'ai_initiatives_research' in research_data:
                research_data['ai_initiatives'] = research_data['ai_initiatives_research']
            
            if 'recent_news_analysis' in research_data:
                research_data['recent_news'] = research_data['recent_news_analysis']
            
            print("✅ AI-powered research completed successfully!")
            print("📊 Generated real insights instead of placeholder content")
            
            return research_data
            
        except Exception as e:
            logger.error(f"Error in AI research generation: {e}")
            print(f"⚠️  AI research generation failed: {e}")
            print("📝 Falling back to manual research prompts")
            
            # Fallback to original placeholder approach with better messaging
            research_data = {
                "company_dossier": f"AI research for {company_name} company dossier needs manual completion. Use enhanced prompts in ai_research_engine.py",
                "industry_analysis": f"Industry analysis for {company_name} needs manual completion. Check ai_research_engine.py for enhanced prompts",
                "competitive_landscape": f"Competitive analysis for {company_name} needs manual completion. Enhanced prompts available",
                "recent_news": f"Recent news analysis for {company_name} needs manual completion. Use AI research engine",
                "business_model": f"Business model analysis for {company_name} needs manual completion",
                "key_challenges": f"Key challenges analysis for {company_name} needs manual completion", 
                "ai_initiatives": f"AI initiatives research for {company_name} needs manual completion"
            }
            
            print("💡 Use the enhanced AI research engine for higher quality results")
            return research_data
    
    def _analyze_network_opportunities(self, company_name: str) -> Dict:
        """
        Network Activation analysis per Never Search Alone methodology.
        
        Identifies:
        - 1st/2nd degree connections at company
        - Potential warm intro paths  
        - Industry contacts who know the company
        - Alumni networks and past work connections
        """
        print("📱 Analyzing LinkedIn connections...")
        print("🔗 Identifying warm introduction paths...")
        print("🎓 Checking alumni networks...")
        
        # This would integrate with LinkedIn API or manual research
        network_data = {
            "first_degree_connections": [],
            "second_degree_connections": [],
            "alumni_connections": [],
            "industry_connections": [],
            "warm_intro_paths": [],
            "recommended_outreach": []
        }
        
        print("📝 Network analysis prepared - manual LinkedIn research required")
        
        return network_data
    
    def _generate_research_summary(self, company_data: Dict):
        """Generate and save research summary to company folder."""
        company_key = company_data["name"].lower().replace(" ", "_")
        company_dir = self.output_dir / company_key
        company_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate Application Research Notes
        research_notes_path = company_dir / "Application_Research_Notes.md"
        
        research_template = f"""# {company_data['name']} - Application Research Notes

## Research Summary
- **Research Date**: {company_data['research_date']}
- **Target Role**: {company_data.get('role_title', 'Not specified')}
- **Priority Score**: {company_data['priority_score']}/40
- **Status**: {company_data['status']}

## Priority Scoring Breakdown
{self._format_priority_scores(company_data.get('priority_breakdown', {}))}

## Company Intelligence
{self._format_research_data(company_data)}

## Network Opportunities
{self._format_network_data(company_data.get('network_opportunities', {}))}

## Next Actions
- [ ] Complete AI-powered company dossier using provided prompts
- [ ] Conduct LinkedIn network analysis
- [ ] Generate application package (resume, cover letter)
- [ ] Identify and reach out to warm connections
- [ ] Prepare cold email campaign

## AI Research Prompts to Execute

### Company Dossier Prompt
```
{self.config['ai_prompts']['company_research'].format(
    company_name=company_data['name'],
    target_role=company_data.get('role_title', 'Senior Product Manager')
)}
```

### Industry Analysis Prompt  
```
{self.config['ai_prompts']['industry_research'].format(
    specific_team='product team',
    company_name=company_data['name'],
    solve_key_problem='scale product growth',
    specific_area='user acquisition and retention'
)}
```

## Notes
- Research completed via Job Search Orchestrator
- Follow up with manual AI research execution
- Update this document with findings
"""
        
        with open(research_notes_path, 'w') as f:
            f.write(research_template)
    
    def _format_priority_scores(self, scores: Dict) -> str:
        """Format priority scores for markdown display."""
        if not scores:
            return "Priority scores not available"
        
        formatted = ""
        for category, score in scores.items():
            formatted += f"- **{category.replace('_', ' ').title()}**: {score}/10\n"
        formatted += f"- **Total**: {sum(scores.values())}/40\n"
        return formatted
    
    def _format_research_data(self, company_data: Dict) -> str:
        """Format research data for markdown display."""
        research_sections = [
            "company_dossier", "industry_analysis", "competitive_landscape",
            "recent_news", "business_model", "key_challenges", "ai_initiatives"
        ]
        
        formatted = ""
        for section in research_sections:
            if section in company_data:
                section_title = section.replace('_', ' ').title()
                formatted += f"### {section_title}\n{company_data[section]}\n\n"
        
        return formatted
    
    def _format_network_data(self, network_data: Dict) -> str:
        """Format network data for markdown display."""
        if not network_data:
            return "Network analysis not completed"
        
        formatted = ""
        network_sections = [
            ("first_degree_connections", "1st Degree Connections"),
            ("second_degree_connections", "2nd Degree Connections"), 
            ("alumni_connections", "Alumni Network"),
            ("warm_intro_paths", "Warm Introduction Paths"),
            ("recommended_outreach", "Recommended Outreach")
        ]
        
        for section_key, section_title in network_sections:
            if section_key in network_data:
                connections = network_data[section_key]
                formatted += f"### {section_title}\n"
                if connections:
                    for connection in connections:
                        formatted += f"- {connection}\n"
                else:
                    formatted += "- None identified\n"
                formatted += "\n"
        
        return formatted

def main():
    """Main CLI interface for the Job Search Orchestrator."""
    parser = argparse.ArgumentParser(description="Job Search Orchestrator - Your AI-powered job search command center")
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Research command
    research_parser = subparsers.add_parser('research', help='Research a company and assess fit')
    research_parser.add_argument('company', help='Company name to research')
    research_parser.add_argument('--role', help='Target role title')
    research_parser.add_argument('--force-refresh', action='store_true', help='Force refresh of existing research')
    research_parser.add_argument('--scores', help='Qualification scores as JSON: {"role_appeal":8,"company_fit":9,"growth_potential":8,"likelihood":7}')
    
    # Apply command
    apply_parser = subparsers.add_parser('apply', help='Generate application package')
    apply_parser.add_argument('company', help='Company name to apply to')
    apply_parser.add_argument('--role', help='Target role title')
    
    # Email command
    email_parser = subparsers.add_parser('email', help='Create cold email campaign')
    email_parser.add_argument('company', help='Company name for email campaign')
    email_parser.add_argument('--target', help='Specific person to email')
    
    # Prep command
    prep_parser = subparsers.add_parser('prep', help='Generate interview preparation materials')
    prep_parser.add_argument('company', help='Company name for interview prep')
    prep_parser.add_argument('--role', help='Target role title')
    
    # Track command
    track_parser = subparsers.add_parser('track', help='View pipeline status and next actions')
    
    # Config command
    config_parser = subparsers.add_parser('config', help='Configure settings and templates')
    config_parser.add_argument('--edit', action='store_true', help='Open config file for editing')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Initialize orchestrator
    orchestrator = JobSearchOrchestrator()
    
    try:
        if args.command == 'research':
            scores = None
            if args.scores:
                try:
                    scores = json.loads(args.scores)
                except json.JSONDecodeError:
                    print("❌ Invalid JSON format for scores. Using interactive mode.")
            result = orchestrator.research_company(args.company, args.role, args.force_refresh, scores)
            print(f"\n✅ Research completed for {args.company}")
            
        elif args.command == 'apply':
            from application_generator import ApplicationGenerator
            generator = ApplicationGenerator(orchestrator.config)
            
            # Load research data if available
            research_data = orchestrator._load_company_data(args.company)
            
            result = generator.generate_application_package(
                args.company, 
                args.role or research_data.get('role_title', 'Product Manager'),
                research_data=research_data
            )
            print(f"\n✅ Application package generated for {args.company}")
            print(f"📁 Files saved to: Applications/{args.company.lower()}/")
            
            # Update pipeline status
            orchestrator._update_pipeline_status(args.company, 'application_generated', True)
            
        elif args.command == 'email':
            from cold_email_system import ColdEmailSystem
            email_system = ColdEmailSystem(orchestrator.config)
            
            # Load research data if available  
            research_data = orchestrator._load_company_data(args.company)
            
            result = email_system.create_email_campaign(
                args.company,
                args.target or research_data.get('role_title', 'Product Manager'),
                research_data=research_data
            )
            print(f"\n✅ Cold email campaign created for {args.company}")
            print(f"📁 Email templates saved to: Applications/{args.company.lower()}/cold_emails/")
            print(f"📧 {len(result.get('emails', []))} personalized emails generated")
            
            # Update pipeline status
            orchestrator._update_pipeline_status(args.company, 'emails_sent', result.get('emails', []))
            
        elif args.command == 'prep':
            from interview_prep_system import InterviewPrepSystem
            prep_system = InterviewPrepSystem(orchestrator.config)
            
            # Load research data if available
            research_data = orchestrator._load_company_data(args.company)
            
            result = prep_system.generate_interview_prep(
                args.company,
                args.role or research_data.get('role_title', 'Product Manager'),
                research_data=research_data
            )
            print(f"\n✅ Interview preparation materials generated for {args.company}")
            print(f"📁 Materials saved to: Applications/{args.company.lower()}/")
            print(f"❓ {len(result.get('question_bank', []))} interview questions prepared")
            print(f"⭐ {len(result.get('star_responses', []))} STAR responses ready")
            
            # Update pipeline status - no specific field for interview prep, but we could add it
            print("📝 Interview preparation complete - ready for scheduling!")
            
        elif args.command == 'track':
            from pipeline_tracker import PipelineTracker
            tracker = PipelineTracker(orchestrator.config)
            
            result = tracker.generate_dashboard() 
            print(f"\n📊 PIPELINE DASHBOARD")
            print("=" * 50)
            
            # Display key metrics
            summary = result.get('pipeline_summary', {})
            print(f"📈 Total Companies: {summary.get('total_companies', 0)}")
            print(f"🔍 Researched: {summary.get('researched', 0)}")
            print(f"📝 Applied: {summary.get('applied', 0)}")
            print(f"📧 Outreach Sent: {summary.get('outreach_sent', 0)}")
            print(f"🎯 Response Rate: {summary.get('response_rate', 0)}%")
            
            # Show next actions
            next_actions = result.get('next_actions', [])
            if next_actions:
                print(f"\n⚡ NEXT ACTIONS ({len(next_actions)})")
                for i, action in enumerate(next_actions[:5], 1):
                    print(f"  {i}. {action.get('description', 'Unknown action')}")
            
            print(f"\n📁 Full dashboard saved to: Pipeline_Dashboard.md")
            print("💡 Run individual commands to take next actions")
            
        elif args.command == 'config':
            if args.edit:
                print(f"📝 Config file location: {orchestrator.config_file}")
                print("Edit the file and restart the orchestrator to apply changes.")
            else:
                print("🚧 Configuration management - Feature coming soon!")
                
    except KeyboardInterrupt:
        print("\n\n👋 Job search orchestrator interrupted. Your progress has been saved.")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error in job search orchestrator: {e}")
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()