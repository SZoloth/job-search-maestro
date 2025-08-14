#!/usr/bin/env python3
"""
Pipeline Tracker and Progress Monitoring System

Comprehensive tracking and analytics system for job search pipeline management.
Provides dashboard views, success metrics analysis, and progress monitoring
for the entire job search automation framework.

This system tracks:
1. Application pipeline status and conversion rates
2. Email campaign performance and response rates
3. Interview scheduling and outcomes
4. Success metrics and ROI analysis
5. Next actions and follow-up management

Usage:
    from pipeline_tracker import PipelineTracker
    
    tracker = PipelineTracker()
    dashboard = tracker.generate_dashboard()
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import logging
from collections import defaultdict

logger = logging.getLogger(__name__)

class PipelineTracker:
    """
    Comprehensive pipeline tracking and progress monitoring system.
    
    Features:
    - Real-time pipeline status dashboard
    - Success metrics analysis and trending
    - Email campaign performance tracking  
    - Interview outcome monitoring
    - Next actions and follow-up management
    - ROI and efficiency analytics
    """
    
    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.pipeline_file = Path("data/application_pipeline.json")
        self.output_dir = Path("Applications")
        
        # Load pipeline data
        self.pipeline_data = self._load_pipeline_data()
        
        # Success metrics targets from config
        self.targets = {
            "response_rate": 0.4,
            "interview_conversion": 0.7,
            "time_per_application": 45,
            "applications_per_week": 5
        }
    
    def _load_pipeline_data(self) -> Dict:
        """Load pipeline data from JSON file."""
        if self.pipeline_file.exists():
            with open(self.pipeline_file, 'r') as f:
                return json.load(f)
        
        # Initialize empty pipeline
        return {
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
    
    def generate_dashboard(self) -> Dict:
        """Generate comprehensive pipeline dashboard."""
        logger.info("Generating pipeline dashboard...")
        
        dashboard = {
            "generated_at": datetime.now().isoformat(),
            "pipeline_summary": self._generate_pipeline_summary(),
            "company_status": self._generate_company_status(),
            "success_metrics": self._generate_success_metrics(),
            "email_performance": self._generate_email_performance(),
            "interview_tracking": self._generate_interview_tracking(),
            "next_actions": self._generate_next_actions(),
            "weekly_progress": self._generate_weekly_progress(),
            "recommendations": self._generate_recommendations()
        }
        
        # Save dashboard to file
        self._save_dashboard(dashboard)
        
        return dashboard
    
    def _generate_pipeline_summary(self) -> Dict:
        """Generate high-level pipeline summary."""
        companies = self.pipeline_data.get("companies", {})
        
        status_counts = defaultdict(int)
        priority_breakdown = defaultdict(int)
        
        for company_data in companies.values():
            status = company_data.get("status", "unknown")
            status_counts[status] += 1
            
            priority = company_data.get("priority_score", 0)
            if priority >= 35:
                priority_breakdown["high"] += 1
            elif priority >= 28:
                priority_breakdown["medium"] += 1
            else:
                priority_breakdown["low"] += 1
        
        total_companies = len(companies)
        
        return {
            "total_companies": total_companies,
            "status_breakdown": dict(status_counts),
            "priority_breakdown": dict(priority_breakdown),
            "completion_rate": self._calculate_completion_rate(),
            "active_opportunities": status_counts.get("researched", 0) + status_counts.get("applied", 0) + status_counts.get("interviewing", 0)
        }
    
    def _generate_company_status(self) -> List[Dict]:
        """Generate detailed company status list."""
        companies = self.pipeline_data.get("companies", {})
        
        company_status = []
        for company_key, company_data in companies.items():
            status_info = {
                "company_name": company_data.get("name", company_key),
                "status": company_data.get("status", "unknown"),
                "priority_score": company_data.get("priority_score", 0),
                "research_date": company_data.get("research_date", ""),
                "last_activity": self._get_last_activity_date(company_data),
                "next_action": self._determine_next_action(company_data),
                "days_since_activity": self._calculate_days_since_activity(company_data),
                "emails_sent": len(company_data.get("emails_sent", [])),
                "interviews_scheduled": len(company_data.get("interviews", [])),
                "response_received": self._has_received_response(company_data)
            }
            company_status.append(status_info)
        
        # Sort by priority score and recent activity
        company_status.sort(key=lambda x: (x["priority_score"], -x["days_since_activity"]), reverse=True)
        
        return company_status
    
    def _generate_success_metrics(self) -> Dict:
        """Generate success metrics analysis."""
        companies = self.pipeline_data.get("companies", {})
        
        # Email metrics
        total_emails = 0
        responses_received = 0
        interviews_from_emails = 0
        
        # Application metrics  
        total_applications = 0
        interviews_scheduled = 0
        offers_received = 0
        
        # Timing metrics
        research_times = []
        application_times = []
        
        for company_data in companies.values():
            emails_sent = company_data.get("emails_sent", [])
            total_emails += len(emails_sent)
            
            if self._has_received_response(company_data):
                responses_received += 1
            
            interviews = company_data.get("interviews", [])
            if interviews:
                interviews_scheduled += 1
                
            if company_data.get("status") == "applied":
                total_applications += 1
            
            if company_data.get("offer_received"):
                offers_received += 1
        
        # Calculate rates
        email_response_rate = responses_received / total_emails if total_emails > 0 else 0
        interview_conversion_rate = interviews_scheduled / total_applications if total_applications > 0 else 0
        offer_conversion_rate = offers_received / interviews_scheduled if interviews_scheduled > 0 else 0
        
        return {
            "email_metrics": {
                "total_sent": total_emails,
                "responses_received": responses_received,
                "response_rate": round(email_response_rate, 3),
                "target_response_rate": self.targets["response_rate"],
                "performance_vs_target": round(email_response_rate / self.targets["response_rate"], 2) if self.targets["response_rate"] > 0 else 0
            },
            "application_metrics": {
                "total_applications": total_applications,
                "interviews_scheduled": interviews_scheduled,
                "interview_conversion_rate": round(interview_conversion_rate, 3),
                "target_conversion_rate": self.targets["interview_conversion"],
                "performance_vs_target": round(interview_conversion_rate / self.targets["interview_conversion"], 2) if self.targets["interview_conversion"] > 0 else 0
            },
            "offer_metrics": {
                "offers_received": offers_received,
                "offer_conversion_rate": round(offer_conversion_rate, 3),
                "pipeline_value": offers_received * 165000  # Assuming $165K average target
            },
            "efficiency_metrics": {
                "average_research_time": round(sum(research_times) / len(research_times), 1) if research_times else 0,
                "average_application_time": round(sum(application_times) / len(application_times), 1) if application_times else 0,
                "target_application_time": self.targets["time_per_application"]
            }
        }
    
    def _generate_email_performance(self) -> Dict:
        """Generate email campaign performance analysis."""
        companies = self.pipeline_data.get("companies", {})
        
        email_campaigns = []
        template_performance = defaultdict(lambda: {"sent": 0, "responses": 0})
        daily_activity = defaultdict(int)
        
        for company_data in companies.values():
            emails_sent = company_data.get("emails_sent", [])
            
            for email in emails_sent:
                campaign_info = {
                    "company": company_data.get("name", "Unknown"),
                    "send_date": email.get("send_date", ""),
                    "template_used": email.get("template", "unknown"),
                    "response_received": email.get("response_received", False),
                    "days_since_sent": self._calculate_days_since(email.get("send_date", "")),
                    "follow_up_sent": email.get("follow_up_sent", False)
                }
                email_campaigns.append(campaign_info)
                
                # Track template performance
                template = email.get("template", "unknown")
                template_performance[template]["sent"] += 1
                if email.get("response_received"):
                    template_performance[template]["responses"] += 1
                
                # Track daily activity
                send_date = email.get("send_date", "")[:10]  # YYYY-MM-DD
                if send_date:
                    daily_activity[send_date] += 1
        
        # Calculate template response rates
        template_stats = {}
        for template, stats in template_performance.items():
            response_rate = stats["responses"] / stats["sent"] if stats["sent"] > 0 else 0
            template_stats[template] = {
                "emails_sent": stats["sent"],
                "responses": stats["responses"], 
                "response_rate": round(response_rate, 3)
            }
        
        return {
            "campaign_details": email_campaigns,
            "template_performance": template_stats,
            "daily_activity": dict(daily_activity),
            "best_performing_template": max(template_stats.items(), key=lambda x: x[1]["response_rate"])[0] if template_stats else "None",
            "total_campaigns": len(email_campaigns),
            "pending_responses": len([c for c in email_campaigns if not c["response_received"] and c["days_since_sent"] <= 14])
        }
    
    def _generate_interview_tracking(self) -> Dict:
        """Generate interview tracking and outcomes."""
        companies = self.pipeline_data.get("companies", {})
        
        interviews = []
        interview_stages = defaultdict(int)
        outcomes = defaultdict(int)
        
        for company_data in companies.values():
            company_interviews = company_data.get("interviews", [])
            
            for interview in company_interviews:
                interview_info = {
                    "company": company_data.get("name", "Unknown"),
                    "date": interview.get("date", ""),
                    "type": interview.get("type", "unknown"),
                    "stage": interview.get("stage", "unknown"),
                    "interviewer": interview.get("interviewer", ""),
                    "outcome": interview.get("outcome", "pending"),
                    "feedback": interview.get("feedback", ""),
                    "next_steps": interview.get("next_steps", "")
                }
                interviews.append(interview_info)
                
                # Track stages and outcomes
                interview_stages[interview.get("stage", "unknown")] += 1
                outcomes[interview.get("outcome", "pending")] += 1
        
        return {
            "scheduled_interviews": len(interviews),
            "interview_details": interviews,
            "stage_breakdown": dict(interview_stages),
            "outcome_breakdown": dict(outcomes),
            "upcoming_interviews": [i for i in interviews if self._is_upcoming_interview(i["date"])],
            "pending_feedback": len([i for i in interviews if i["outcome"] == "pending"]),
            "success_rate": round(outcomes.get("advanced", 0) / len(interviews), 3) if interviews else 0
        }
    
    def _generate_next_actions(self) -> List[Dict]:
        """Generate prioritized next actions list."""
        companies = self.pipeline_data.get("companies", {})
        next_actions = []
        
        current_date = datetime.now()
        
        for company_key, company_data in companies.items():
            company_name = company_data.get("name", company_key)
            status = company_data.get("status", "unknown")
            
            # Research follow-ups
            if status == "researched" and not company_data.get("application_generated"):
                next_actions.append({
                    "priority": "high",
                    "action": "Generate application package",
                    "company": company_name,
                    "due_date": self._calculate_due_date(company_data.get("research_date"), days=2),
                    "details": "Research completed, ready for application generation"
                })
            
            # Email follow-ups
            emails_sent = company_data.get("emails_sent", [])
            for email in emails_sent:
                send_date_str = email.get("send_date", "")
                if send_date_str and not email.get("response_received"):
                    send_date = datetime.fromisoformat(send_date_str.replace('Z', '+00:00'))
                    days_since = (current_date - send_date).days
                    
                    if days_since >= 7 and not email.get("follow_up_sent"):
                        next_actions.append({
                            "priority": "medium",
                            "action": "Send follow-up email",
                            "company": company_name,
                            "due_date": send_date_str,
                            "details": f"Original email sent {days_since} days ago"
                        })
            
            # Interview follow-ups
            interviews = company_data.get("interviews", [])
            for interview in interviews:
                if interview.get("outcome") == "pending":
                    interview_date = interview.get("date", "")
                    if interview_date:
                        next_actions.append({
                            "priority": "high",
                            "action": "Follow up on interview outcome",
                            "company": company_name,
                            "due_date": interview_date,
                            "details": f"{interview.get('stage', 'Interview')} with {interview.get('interviewer', 'TBD')}"
                        })
        
        # Sort by priority and due date
        priority_order = {"high": 3, "medium": 2, "low": 1}
        next_actions.sort(key=lambda x: (priority_order.get(x["priority"], 0), x["due_date"]), reverse=True)
        
        return next_actions[:20]  # Return top 20 actions
    
    def _generate_weekly_progress(self) -> Dict:
        """Generate weekly progress analysis."""
        companies = self.pipeline_data.get("companies", {})
        
        # Get current week boundaries
        today = datetime.now()
        week_start = today - timedelta(days=today.weekday())
        week_end = week_start + timedelta(days=6)
        
        weekly_stats = {
            "companies_researched": 0,
            "applications_submitted": 0,
            "emails_sent": 0,
            "responses_received": 0,
            "interviews_scheduled": 0,
            "target_applications": self.targets["applications_per_week"]
        }
        
        for company_data in companies.values():
            # Count research completed this week
            research_date_str = company_data.get("research_date", "")
            if research_date_str:
                research_date = datetime.fromisoformat(research_date_str.replace('Z', '+00:00'))
                if week_start <= research_date <= week_end:
                    weekly_stats["companies_researched"] += 1
            
            # Count emails sent this week
            emails_sent = company_data.get("emails_sent", [])
            for email in emails_sent:
                send_date_str = email.get("send_date", "")
                if send_date_str:
                    send_date = datetime.fromisoformat(send_date_str.replace('Z', '+00:00'))
                    if week_start <= send_date <= week_end:
                        weekly_stats["emails_sent"] += 1
                        if email.get("response_received"):
                            weekly_stats["responses_received"] += 1
            
            # Count interviews scheduled this week
            interviews = company_data.get("interviews", [])
            for interview in interviews:
                schedule_date_str = interview.get("scheduled_date", interview.get("date", ""))
                if schedule_date_str:
                    schedule_date = datetime.fromisoformat(schedule_date_str.replace('Z', '+00:00'))
                    if week_start <= schedule_date <= week_end:
                        weekly_stats["interviews_scheduled"] += 1
        
        # Calculate progress vs targets
        application_progress = weekly_stats["applications_submitted"] / weekly_stats["target_applications"]
        
        return {
            "week_start": week_start.isoformat(),
            "week_end": week_end.isoformat(),
            "weekly_stats": weekly_stats,
            "progress_vs_target": round(application_progress, 2),
            "on_track": application_progress >= 0.8
        }
    
    def _generate_recommendations(self) -> List[Dict]:
        """Generate actionable recommendations based on pipeline analysis."""
        success_metrics = self._generate_success_metrics()
        email_performance = self._generate_email_performance()
        
        recommendations = []
        
        # Email response rate recommendations
        email_response_rate = success_metrics["email_metrics"]["response_rate"]
        target_response_rate = success_metrics["email_metrics"]["target_response_rate"]
        
        if email_response_rate < target_response_rate * 0.8:
            recommendations.append({
                "category": "email_optimization",
                "priority": "high",
                "title": "Improve Email Response Rate",
                "description": f"Current response rate ({email_response_rate:.1%}) is below target ({target_response_rate:.1%})",
                "actions": [
                    "Review email templates for clarity and personalization",
                    "Ensure emails are under 200 words with clear ask",
                    "Focus on 1st/2nd degree LinkedIn connections",
                    "Improve company research depth for better personalization"
                ]
            })
        
        # Application volume recommendations
        weekly_progress = self._generate_weekly_progress()
        if not weekly_progress["on_track"]:
            recommendations.append({
                "category": "volume_optimization",
                "priority": "medium",
                "title": "Increase Application Volume",
                "description": f"Behind target applications per week ({weekly_progress['weekly_stats']['applications_submitted']} vs {weekly_progress['weekly_stats']['target_applications']})",
                "actions": [
                    "Research 2-3 additional companies this week",
                    "Focus on companies with higher priority scores",
                    "Use automation system to reduce time per application"
                ]
            })
        
        # Pipeline stage recommendations
        pipeline_summary = self._generate_pipeline_summary()
        researched_count = pipeline_summary["status_breakdown"].get("researched", 0)
        
        if researched_count > 3:
            recommendations.append({
                "category": "pipeline_efficiency",
                "priority": "medium", 
                "title": "Convert Research to Applications",
                "description": f"{researched_count} companies researched but not yet applied to",
                "actions": [
                    "Generate application packages for researched companies",
                    "Prioritize companies with scores ≥ 32",
                    "Set aside 2 hours for application generation"
                ]
            })
        
        # Template performance recommendations
        if email_performance["template_performance"]:
            best_template = email_performance["best_performing_template"]
            recommendations.append({
                "category": "template_optimization",
                "priority": "low",
                "title": "Optimize Email Templates",
                "description": f"'{best_template}' template performing best",
                "actions": [
                    f"Use '{best_template}' template for similar company types",
                    "A/B test variations of high-performing templates",
                    "Archive or improve low-performing templates"
                ]
            })
        
        return recommendations
    
    def _calculate_completion_rate(self) -> float:
        """Calculate overall pipeline completion rate."""
        companies = self.pipeline_data.get("companies", {})
        if not companies:
            return 0.0
        
        completed_stages = 0
        total_possible_stages = len(companies) * 5  # 5 stages per company
        
        for company_data in companies.values():
            status = company_data.get("status", "unknown")
            
            if status in ["researched", "applied", "interviewing", "offered", "hired"]:
                completed_stages += 1
            if status in ["applied", "interviewing", "offered", "hired"]:
                completed_stages += 1
            if status in ["interviewing", "offered", "hired"]:
                completed_stages += 1
            if status in ["offered", "hired"]:
                completed_stages += 1
            if status == "hired":
                completed_stages += 1
        
        return round(completed_stages / total_possible_stages, 3) if total_possible_stages > 0 else 0
    
    def _get_last_activity_date(self, company_data: Dict) -> str:
        """Get the last activity date for a company."""
        dates = []
        
        research_date = company_data.get("research_date")
        if research_date:
            dates.append(research_date)
        
        emails = company_data.get("emails_sent", [])
        for email in emails:
            if email.get("send_date"):
                dates.append(email["send_date"])
        
        interviews = company_data.get("interviews", [])
        for interview in interviews:
            if interview.get("date"):
                dates.append(interview["date"])
        
        return max(dates) if dates else ""
    
    def _determine_next_action(self, company_data: Dict) -> str:
        """Determine next action for a company based on current status."""
        status = company_data.get("status", "unknown")
        
        action_map = {
            "researching": "Complete company research",
            "researched": "Generate application package",
            "applied": "Send cold email campaign", 
            "email_sent": "Monitor for responses",
            "responded": "Schedule interview",
            "interviewing": "Follow up on interview outcome",
            "offered": "Negotiate and decide",
            "hired": "Complete - Success!",
            "rejected": "Archive and learn from feedback"
        }
        
        return action_map.get(status, "Determine status and next steps")
    
    def _calculate_days_since_activity(self, company_data: Dict) -> int:
        """Calculate days since last activity."""
        last_activity = self._get_last_activity_date(company_data)
        if not last_activity:
            return 0
        
        try:
            activity_date = datetime.fromisoformat(last_activity.replace('Z', '+00:00'))
            return (datetime.now() - activity_date).days
        except:
            return 0
    
    def _has_received_response(self, company_data: Dict) -> bool:
        """Check if any email response has been received."""
        emails = company_data.get("emails_sent", [])
        return any(email.get("response_received", False) for email in emails)
    
    def _calculate_days_since(self, date_string: str) -> int:
        """Calculate days since a given date string."""
        if not date_string:
            return 0
        
        try:
            date = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
            return (datetime.now() - date).days
        except:
            return 0
    
    def _is_upcoming_interview(self, date_string: str) -> bool:
        """Check if an interview is upcoming (within next 14 days)."""
        if not date_string:
            return False
        
        try:
            interview_date = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
            days_until = (interview_date - datetime.now()).days
            return 0 <= days_until <= 14
        except:
            return False
    
    def _calculate_due_date(self, base_date_str: str, days: int) -> str:
        """Calculate due date by adding days to base date."""
        if not base_date_str:
            return datetime.now().isoformat()
        
        try:
            base_date = datetime.fromisoformat(base_date_str.replace('Z', '+00:00'))
            due_date = base_date + timedelta(days=days)
            return due_date.isoformat()
        except:
            return datetime.now().isoformat()
    
    def _save_dashboard(self, dashboard: Dict) -> Path:
        """Save dashboard to markdown file."""
        output_file = Path("Pipeline_Dashboard.md")
        
        dashboard_content = f"""# Job Search Pipeline Dashboard

**Generated:** {dashboard['generated_at']}

## 📊 Pipeline Summary

{self._format_pipeline_summary(dashboard['pipeline_summary'])}

## 🏢 Company Status

{self._format_company_status(dashboard['company_status'])}

## 📈 Success Metrics

{self._format_success_metrics(dashboard['success_metrics'])}

## 📧 Email Performance

{self._format_email_performance(dashboard['email_performance'])}

## 🎯 Interview Tracking

{self._format_interview_tracking(dashboard['interview_tracking'])}

## ⏰ Next Actions

{self._format_next_actions(dashboard['next_actions'])}

## 📅 Weekly Progress

{self._format_weekly_progress(dashboard['weekly_progress'])}

## 💡 Recommendations

{self._format_recommendations(dashboard['recommendations'])}

---

*Dashboard auto-generated by Job Search Pipeline Tracker*
*Use `python job_search_orchestrator.py track` to refresh*
"""
        
        with open(output_file, 'w') as f:
            f.write(dashboard_content)
        
        logger.info(f"Dashboard saved to: {output_file}")
        return output_file
    
    def _format_pipeline_summary(self, summary: Dict) -> str:
        """Format pipeline summary for markdown."""
        return f"""**Total Companies:** {summary['total_companies']}  
**Active Opportunities:** {summary['active_opportunities']}  
**Completion Rate:** {summary['completion_rate']:.1%}

### Status Breakdown
{self._format_dict_as_list(summary['status_breakdown'])}

### Priority Breakdown
{self._format_dict_as_list(summary['priority_breakdown'])}"""
    
    def _format_company_status(self, companies: List[Dict]) -> str:
        """Format company status table."""
        if not companies:
            return "No companies in pipeline"
        
        formatted = "| Company | Status | Priority | Days Since Activity | Next Action |\n"
        formatted += "|---------|--------|----------|---------------------|-------------|\n"
        
        for company in companies[:15]:  # Show top 15
            formatted += f"| {company['company_name']} | {company['status']} | {company['priority_score']}/40 | {company['days_since_activity']} | {company['next_action']} |\n"
        
        if len(companies) > 15:
            formatted += f"\n*Showing top 15 of {len(companies)} companies*"
        
        return formatted
    
    def _format_success_metrics(self, metrics: Dict) -> str:
        """Format success metrics section."""
        email = metrics['email_metrics']
        application = metrics['application_metrics']
        
        return f"""### Email Campaign Performance
- **Emails Sent:** {email['total_sent']}
- **Response Rate:** {email['response_rate']:.1%} (Target: {email['target_response_rate']:.1%})
- **Performance vs Target:** {email['performance_vs_target']:.1f}x

### Application Conversion  
- **Applications Submitted:** {application['total_applications']}
- **Interviews Scheduled:** {application['interviews_scheduled']}
- **Interview Conversion:** {application['interview_conversion_rate']:.1%} (Target: {application['target_conversion_rate']:.1%})
- **Performance vs Target:** {application['performance_vs_target']:.1f}x"""
    
    def _format_email_performance(self, performance: Dict) -> str:
        """Format email performance analysis."""
        formatted = f"**Total Campaigns:** {performance['total_campaigns']}  \n"
        formatted += f"**Best Template:** {performance['best_performing_template']}  \n"
        formatted += f"**Pending Responses:** {performance['pending_responses']}  \n\n"
        
        if performance['template_performance']:
            formatted += "### Template Performance\n"
            for template, stats in performance['template_performance'].items():
                formatted += f"- **{template}:** {stats['response_rate']:.1%} ({stats['responses']}/{stats['emails_sent']})\n"
        
        return formatted
    
    def _format_interview_tracking(self, tracking: Dict) -> str:
        """Format interview tracking section."""
        formatted = f"**Scheduled Interviews:** {tracking['scheduled_interviews']}  \n"
        formatted += f"**Success Rate:** {tracking['success_rate']:.1%}  \n"
        formatted += f"**Pending Feedback:** {tracking['pending_feedback']}  \n\n"
        
        if tracking['upcoming_interviews']:
            formatted += "### Upcoming Interviews\n"
            for interview in tracking['upcoming_interviews']:
                formatted += f"- **{interview['company']}:** {interview['date']} - {interview['type']}\n"
        
        return formatted
    
    def _format_next_actions(self, actions: List[Dict]) -> str:
        """Format next actions list."""
        if not actions:
            return "No immediate actions required"
        
        formatted = ""
        for action in actions[:10]:  # Show top 10
            priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(action['priority'], "⚪")
            formatted += f"{priority_emoji} **{action['action']}** - {action['company']}  \n"
            formatted += f"   {action['details']}  \n\n"
        
        return formatted
    
    def _format_weekly_progress(self, progress: Dict) -> str:
        """Format weekly progress section."""
        stats = progress['weekly_stats']
        status_emoji = "✅" if progress['on_track'] else "⚠️"
        
        return f"""{status_emoji} **Week Progress:** {progress['progress_vs_target']:.1%} of target

- **Companies Researched:** {stats['companies_researched']}
- **Emails Sent:** {stats['emails_sent']}
- **Responses Received:** {stats['responses_received']}
- **Interviews Scheduled:** {stats['interviews_scheduled']}

**Target Applications/Week:** {stats['target_applications']}"""
    
    def _format_recommendations(self, recommendations: List[Dict]) -> str:
        """Format recommendations section."""
        if not recommendations:
            return "No specific recommendations at this time"
        
        formatted = ""
        for rec in recommendations:
            priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(rec['priority'], "⚪")
            formatted += f"{priority_emoji} **{rec['title']}**  \n"
            formatted += f"{rec['description']}  \n\n"
            formatted += "Actions:  \n"
            for action in rec['actions']:
                formatted += f"- {action}  \n"
            formatted += "\n"
        
        return formatted
    
    def _format_dict_as_list(self, data: Dict) -> str:
        """Format dictionary as markdown list."""
        if not data:
            return "- None"
        
        formatted = ""
        for key, value in data.items():
            formatted += f"- **{key.replace('_', ' ').title()}:** {value}\n"
        
        return formatted

# Example usage and CLI interface
if __name__ == "__main__":
    tracker = PipelineTracker()
    dashboard = tracker.generate_dashboard()
    
    print("📊 Job Search Pipeline Dashboard Generated")
    print(f"📁 Saved to: Pipeline_Dashboard.md")
    print(f"🏢 Companies tracked: {dashboard['pipeline_summary']['total_companies']}")
    print(f"📧 Email response rate: {dashboard['success_metrics']['email_metrics']['response_rate']:.1%}")
    print(f"🎯 Active opportunities: {dashboard['pipeline_summary']['active_opportunities']}")
    
    # Show top next actions
    next_actions = dashboard['next_actions'][:5]
    if next_actions:
        print(f"\n⏰ Top 5 Next Actions:")
        for i, action in enumerate(next_actions, 1):
            print(f"{i}. {action['action']} - {action['company']}")
    
    print(f"\n✅ Dashboard ready for review!")