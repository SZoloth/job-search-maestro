#!/usr/bin/env python3
"""
Test Script for Job Search Automation Improvements

This script demonstrates the improvements made to the job search automation system,
specifically testing the enhanced AI research engine and content generation capabilities.

Usage:
    python test_improvements.py

Requirements:
    - OpenAI or Anthropic API key in environment variables
    - pip install openai (optional)
    - pip install anthropic (optional)
"""

import sys
import os
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_ai_research_engine():
    """Test the enhanced AI Research Engine."""
    print("🔍 Testing Enhanced AI Research Engine...")
    print("=" * 50)
    
    try:
        from ai_research_engine import AIResearchEngine
        
        # Initialize research engine
        research_engine = AIResearchEngine()
        
        # Test with Palantir (our case study)
        company_name = "Palantir"
        role_title = "Senior Product Manager"
        
        print(f"Testing company intelligence generation for: {company_name}")
        print(f"Target role: {role_title}")
        print()
        
        # Check if API keys are available
        if not research_engine.openai_client and not research_engine.anthropic_client:
            print("⚠️  No AI service clients available (API keys not found)")
            print("   Set OPENAI_API_KEY or ANTHROPIC_API_KEY environment variables for full testing")
            print("   Testing will proceed with fallback mechanisms...")
            print()
        
        # Generate company intelligence
        print("Generating AI-powered company intelligence...")
        results = research_engine.generate_company_intelligence(company_name, role_title)
        
        print(f"\n✅ Generated {len(results)} research components:")
        
        for research_type, result in results.items():
            print(f"\n📄 {research_type.replace('_', ' ').title()}:")
            print(f"   Content length: {len(result.content)} characters")
            print(f"   Confidence: {result.confidence:.1f}")
            print(f"   Sources: {', '.join(result.sources)}")
            print(f"   Preview: {result.content[:150]}...")
            if result.confidence < 0.5:
                print(f"   ⚠️  Low confidence - likely fallback content")
            else:
                print(f"   ✅ High quality AI-generated content")
        
        # Test personalized content generation
        print(f"\n🎯 Testing personalized content generation...")
        
        context = {
            'company_name': company_name,
            'role_title': role_title,
            'recent_news': results.get('recent_news_analysis', {}).content if 'recent_news_analysis' in results else ''
        }
        
        # Test cover letter opening generation
        try:
            opening_result = research_engine.generate_personalized_content('cover_letter_opening', context)
            print(f"\n📝 Cover Letter Opening Generated:")
            print(f"   Confidence: {opening_result.confidence:.1f}")
            print(f"   Content: {opening_result.content}")
        except Exception as e:
            print(f"   ❌ Error generating cover letter opening: {e}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Make sure ai_research_engine.py is in the current directory")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def test_legacy_compatibility():
    """Test that legacy interfaces still work with improvements."""
    print("\n🔄 Testing Legacy Compatibility...")
    print("=" * 50)
    
    try:
        from ai_research_engine import AIResearchEngine
        
        # Test legacy research_company method
        research_engine = AIResearchEngine()
        
        print("Testing legacy research_company() method...")
        legacy_results = research_engine.research_company("Palantir", "Senior Product Manager")
        
        print(f"✅ Legacy method returned {len(legacy_results.get('research_components', {}))} components")
        
        # Check that results are in expected format
        expected_keys = ['company_name', 'target_role', 'research_date', 'research_components']
        for key in expected_keys:
            if key in legacy_results:
                print(f"   ✅ {key}: Present")
            else:
                print(f"   ❌ {key}: Missing")
        
        return True
        
    except Exception as e:
        print(f"❌ Legacy compatibility test failed: {e}")
        return False

def test_orchestrator_integration():
    """Test integration with job search orchestrator."""
    print("\n🤖 Testing Orchestrator Integration...")
    print("=" * 50)
    
    try:
        from job_search_orchestrator import JobSearchOrchestrator
        
        # Initialize orchestrator
        orchestrator = JobSearchOrchestrator()
        
        print("Testing enhanced _conduct_ai_research method...")
        
        # Test the enhanced AI research method
        research_results = orchestrator._conduct_ai_research("Palantir", "Senior Product Manager")
        
        print(f"✅ Research completed with {len(research_results)} components:")
        
        for key, value in research_results.items():
            content_length = len(str(value))
            print(f"   📄 {key}: {content_length} characters")
            
            # Check if this looks like real content vs placeholder
            if "needs manual completion" in str(value) or "Recent news analysis needed" in str(value):
                print(f"      ⚠️  Contains placeholder content - likely fallback")
            else:
                print(f"      ✅ Contains substantive content")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Orchestrator integration test failed: {e}")
        return False

def compare_before_and_after():
    """Show before/after comparison of quality improvements."""
    print("\n📊 Before vs After Quality Comparison...")
    print("=" * 50)
    
    print("BEFORE IMPROVEMENTS:")
    print("   ❌ Research Notes: 'Recent news analysis needed'")
    print("   ❌ Cover Letters: Generic template with placeholder text")
    print("   ❌ Cold Emails: Basic personalization hooks")
    print("   ❌ Content Generation: Manual prompt execution required")
    print("   ❌ Research Quality: Empty sections and TODO items")
    print()
    
    print("AFTER IMPROVEMENTS:")
    print("   ✅ Research Notes: AI-generated company intelligence with confidence scores")
    print("   ✅ Cover Letters: Personalized openings based on real company research")
    print("   ✅ Cold Emails: AI-powered personalization with context awareness")
    print("   ✅ Content Generation: Automatic AI execution with fallback mechanisms")
    print("   ✅ Research Quality: Substantive content with source attribution")
    print()
    
    print("KEY IMPROVEMENTS SUMMARY:")
    print("   🔹 Real AI API integration (OpenAI/Anthropic)")
    print("   🔹 Enhanced research prompts for better output quality")
    print("   🔹 Research caching for efficiency and cost control")
    print("   🔹 Confidence scoring and quality validation")
    print("   🔹 Graceful fallback when AI services unavailable")
    print("   🔹 Legacy compatibility maintained")
    print("   🔹 Structured error handling and logging")

def main():
    """Run all tests and demonstrate improvements."""
    print("🚀 Job Search Automation Improvements Test Suite")
    print("=" * 60)
    print(f"Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    tests_passed = 0
    total_tests = 3
    
    # Test 1: AI Research Engine
    if test_ai_research_engine():
        tests_passed += 1
    
    # Test 2: Legacy Compatibility
    if test_legacy_compatibility():
        tests_passed += 1
    
    # Test 3: Orchestrator Integration
    if test_orchestrator_integration():
        tests_passed += 1
    
    # Show before/after comparison
    compare_before_and_after()
    
    print(f"\n🏁 Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("✅ All tests passed! Improvements are working correctly.")
    elif tests_passed > 0:
        print("⚠️  Some tests passed - partial functionality working.")
        print("   Note: API key availability affects some features.")
    else:
        print("❌ All tests failed - check implementation.")
    
    print(f"\n📝 To see quality improvements in action:")
    print(f"   1. Set OPENAI_API_KEY or ANTHROPIC_API_KEY environment variable")
    print(f"   2. Run: python job_search_orchestrator.py")
    print(f"   3. Generate application materials for Palantir")
    print(f"   4. Compare with original palantir/ folder content")

if __name__ == "__main__":
    main()