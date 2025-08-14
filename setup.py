#!/usr/bin/env python3
"""
Job Search Orchestrator Setup Script

This script helps new users initialize their personal information
and customize the job search orchestrator template for their use.
"""

import json
import os
import sys
from pathlib import Path

def welcome_message():
    """Display welcome message and overview"""
    print("=" * 60)
    print("🎯 Welcome to Job Search Orchestrator Setup!")
    print("=" * 60)
    print()
    print("This setup will help you customize the template with your personal")
    print("information and career goals. You can always modify these settings")
    print("later by editing the configuration files directly.")
    print()
    print("Let's get started!")
    print()

def get_user_input(prompt, default="", required=True):
    """Get user input with optional default value"""
    while True:
        if default:
            user_input = input(f"{prompt} [{default}]: ").strip()
            if not user_input:
                return default
        else:
            user_input = input(f"{prompt}: ").strip()
        
        if user_input or not required:
            return user_input
        
        if required:
            print("This field is required. Please enter a value.")

def get_list_input(prompt, default_items=None):
    """Get list input from user"""
    print(f"\n{prompt}")
    if default_items:
        print("Default options (press Enter to keep, or provide new ones):")
        for i, item in enumerate(default_items, 1):
            print(f"  {i}. {item}")
    
    print("\nEnter items separated by commas, or press Enter for defaults:")
    user_input = input("> ").strip()
    
    if not user_input and default_items:
        return default_items
    elif user_input:
        return [item.strip() for item in user_input.split(',') if item.strip()]
    else:
        return default_items or []

def setup_user_profile():
    """Collect user profile information"""
    print("\n📝 Personal Information")
    print("-" * 30)
    
    profile = {}
    
    # Basic contact info
    profile['name'] = get_user_input("Full name")
    profile['email'] = get_user_input("Email address")
    profile['phone'] = get_user_input("Phone number (e.g., 555-123-4567)")
    
    linkedin = get_user_input("LinkedIn username (just the username part)", 
                            default="your-linkedin-username")
    profile['linkedin'] = f"linkedin.com/in/{linkedin}/"
    
    # Career targets
    print("\n🎯 Career Targets")
    print("-" * 20)
    
    default_roles = [
        "Senior Product Manager",
        "Growth Product Manager", 
        "Principal Product Manager",
        "Director of Product"
    ]
    profile['target_roles'] = get_list_input("Target job titles", default_roles)
    
    default_industries = [
        "Healthcare Technology",
        "Consumer Products",
        "AI/ML Companies", 
        "EdTech",
        "FinTech",
        "SaaS/Enterprise Software"
    ]
    profile['target_industries'] = get_list_input("Target industries", default_industries)
    
    profile['target_company_size'] = get_user_input(
        "Preferred company size", 
        default="50-500 employees"
    )
    
    profile['remote_preference'] = get_user_input(
        "Remote work preference",
        default="Fully remote or flexible hybrid"
    )
    
    profile['salary_range'] = get_user_input(
        "Target salary range",
        default="$150-180K base with meaningful equity"
    )
    
    # Skills
    default_skills = [
        "Product Strategy",
        "Growth Strategy",
        "User Research", 
        "Data Analysis",
        "Cross-functional Leadership",
        "Stakeholder Management"
    ]
    profile['key_skills'] = get_list_input("Key professional skills", default_skills)
    
    return profile

def update_config_file(profile):
    """Update the configuration file with user profile"""
    config_path = Path("config/job_search_config.json")
    
    # Load existing config
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        print(f"Error: Could not find {config_path}")
        return False
    
    # Update user profile section
    config['user_profile'].update(profile)
    
    # Write back to file
    try:
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        print(f"✅ Configuration updated in {config_path}")
        return True
    except Exception as e:
        print(f"❌ Error updating configuration: {e}")
        return False

def create_personal_resume():
    """Create personalized resume template"""
    print("\n📄 Resume Template Setup")
    print("-" * 30)
    
    resume_source = Path("templates/resume_base.md")
    resume_target = Path("templates/my_resume.md")
    
    try:
        # Copy template
        with open(resume_source, 'r') as f:
            resume_content = f.read()
        
        with open(resume_target, 'w') as f:
            f.write(resume_content)
        
        print(f"✅ Personal resume template created: {resume_target}")
        print("   Edit this file to add your specific experience and achievements")
        return True
    except Exception as e:
        print(f"❌ Error creating resume template: {e}")
        return False

def create_example_application():
    """Create example application folder structure"""
    print("\n📁 Application Structure Setup")
    print("-" * 35)
    
    example_path = Path("Applications/00-example-company")
    
    try:
        example_path.mkdir(parents=True, exist_ok=True)
        
        # Create example files
        files_to_create = [
            ("Application_Research_Notes.md", "# Company Research Notes\n\n*Replace with your research findings*"),
            ("Company_Resume.md", "# Customized Resume\n\n*Copy from templates/my_resume.md and customize*"),
            ("Company_Cover_Letter.md", "# Cover Letter\n\n*Generate using the system or write manually*"),
            ("Cold_Email_Campaign.md", "# Email Campaign\n\n*Generated cold emails and tracking*"),
            ("Interview_Preparation_Guide.md", "# Interview Prep\n\n*Company-specific questions and responses*")
        ]
        
        for filename, content in files_to_create:
            file_path = example_path / filename
            with open(file_path, 'w') as f:
                f.write(content)
        
        print(f"✅ Example application folder created: {example_path}")
        print("   Use this as a template for organizing each company application")
        return True
    except Exception as e:
        print(f"❌ Error creating application structure: {e}")
        return False

def final_instructions():
    """Display final setup instructions"""
    print("\n" + "=" * 60)
    print("🎉 Setup Complete!")
    print("=" * 60)
    print()
    print("Next Steps:")
    print()
    print("1. 📝 Complete your resume:")
    print("   - Edit templates/my_resume.md with your experience")
    print("   - Add specific achievements with quantified metrics")
    print()
    print("2. 📚 Build your case stories:")
    print("   - Edit experience/Case_Stories_Repository.md")
    print("   - Create 3-5 STAR method stories")
    print()
    print("3. ✉️ Customize email templates:")
    print("   - Update achievement examples in templates/email_templates.json")
    print("   - Replace placeholder accomplishments with your own")
    print()
    print("4. 🚀 Test the system:")
    print("   - Try: python job_search_orchestrator.py research \"Test Company\"")
    print("   - Review generated materials and refine as needed")
    print()
    print("5. 📖 Read the documentation:")
    print("   - README.md for usage guide")
    print("   - SYSTEM_README.md for technical details")
    print()
    print("Questions? Check the troubleshooting section in README.md")
    print()

def main():
    """Main setup function"""
    # Check if we're in the right directory
    if not Path("job_search_orchestrator.py").exists():
        print("❌ Please run this script from the job-search-orchestrator directory")
        sys.exit(1)
    
    welcome_message()
    
    # Get user profile
    profile = setup_user_profile()
    
    # Update configuration
    config_success = update_config_file(profile)
    
    # Create personal templates
    resume_success = create_personal_resume()
    
    # Create example structure
    structure_success = create_example_application()
    
    # Final instructions
    final_instructions()
    
    if all([config_success, resume_success, structure_success]):
        print("✅ All setup tasks completed successfully!")
        print("You're ready to start your systematic job search!")
    else:
        print("⚠️  Some setup tasks had issues. Check the messages above.")
        print("You can complete the setup manually or run this script again.")

if __name__ == "__main__":
    main()
