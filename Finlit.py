"""
FinLit: Personal Finance Education Tool
Cattolica University Application Project
Ahmed Raza - Pakistan
"""

import json
import math
from datetime import datetime
from typing import Dict, List, Tuple

class FinanceCalculator:
    """Basic financial calculations anyone can understand"""
    
    def __init__(self, country="global"):
        self.country = country.lower()
        self.setup_country_rules()
    
    def setup_country_rules(self):
        """Simple country-specific financial rules"""
        self.rules = {
            "pakistan": {
                "emergency_months": 6,
                "common_investments": ["Gold", "Property", "National Savings"],
                "inflation_rate": 0.20,  # 20% approximate
                "family_support": True
            },
            "italy": {
                "emergency_months": 3,
                "common_investments": ["BTP Bonds", "ETFs", "Pension Funds"],
                "inflation_rate": 0.03,  # 3% approximate
                "family_support": False
            },
            "global": {
                "emergency_months": 3,
                "common_investments": ["Savings Account", "Index Funds"],
                "inflation_rate": 0.05,
                "family_support": False
            }
        }
    
    def calculate_emergency_fund(self, monthly_expenses: float) -> Dict:
        """Calculate emergency fund needed"""
        target_months = self.rules.get(self.country, self.rules["global"])["emergency_months"]
        target_amount = monthly_expenses * target_months
        
        return {
            "target_months": target_months,
            "target_amount": round(target_amount, 2),
            "explanation": f"In {self.country.title()}, aim for {target_months} months of expenses saved"
        }
    
    def calculate_savings_goal(self, 
                              target_amount: float, 
                              monthly_saving: float, 
                              current_savings: float = 0) -> Dict:
        """Calculate how long to reach savings goal"""
        remaining = target_amount - current_savings
        
        if monthly_saving <= 0:
            return {"error": "Monthly saving must be positive"}
        
        months_needed = remaining / monthly_saving
        years_needed = months_needed / 12
        
        # Adjust for inflation
        inflation_rate = self.rules.get(self.country, self.rules["global"])["inflation_rate"]
        real_months_needed = months_needed * (1 + inflation_rate)
        
        return {
            "months_needed": math.ceil(months_needed),
            "years_needed": round(years_needed, 1),
            "adjusted_months": math.ceil(real_months_needed),
            "monthly_saving": monthly_saving,
            "total_saved": current_savings + (monthly_saving * months_needed)
        }
    
    def calculate_debt_payoff(self, 
                             debt_amount: float, 
                             monthly_payment: float,
                             interest_rate: float = 0.12) -> Dict:
        """Calculate debt payoff timeline"""
        if monthly_payment <= 0:
            return {"error": "Monthly payment must be positive"}
        
        # Simple interest calculation (approximate)
        months = 0
        remaining = debt_amount
        total_interest = 0
        
        while remaining > 0 and months < 600:  # Max 50 years
            interest = remaining * (interest_rate / 12)
            principal_payment = monthly_payment - interest
            
            if principal_payment <= 0:
                return {"error": "Payment too small - not covering interest"}
            
            remaining -= principal_payment
            total_interest += interest
            months += 1
        
        return {
            "months_to_payoff": months,
            "years_to_payoff": round(months / 12, 1),
            "total_interest": round(total_interest, 2),
            "total_paid": round(debt_amount + total_interest, 2)
        }
    
    def calculate_compound_interest(self,
                                   principal: float,
                                   monthly_contribution: float,
                                   years: int,
                                   annual_return: float = 0.08) -> Dict:
        """Calculate compound interest growth"""
        monthly_rate = annual_return / 12
        months = years * 12
        
        future_value = principal
        for month in range(months):
            future_value = future_value * (1 + monthly_rate) + monthly_contribution
        
        total_contributions = principal + (monthly_contribution * months)
        interest_earned = future_value - total_contributions
        
        return {
            "future_value": round(future_value, 2),
            "total_contributions": round(total_contributions, 2),
            "interest_earned": round(interest_earned, 2),
            "growth_multiple": round(future_value / total_contributions, 2)
        }

class BudgetPlanner:
    """Simple budget planning tool"""
    
    def __init__(self, country="global"):
        self.country = country
        self.setup_default_budgets()
    
    def setup_default_budgets(self):
        """Country-specific budget templates"""
        self.templates = {
            "pakistan": {
                "needs_percentage": 50,   # Housing, food, utilities
                "wants_percentage": 30,   # Entertainment, dining out
                "savings_percentage": 20  # Savings and debt repayment
            },
            "italy": {
                "needs_percentage": 40,   # Lower due to social services
                "wants_percentage": 30,
                "savings_percentage": 30
            },
            "global": {
                "needs_percentage": 50,
                "wants_percentage": 30,
                "savings_percentage": 20
            }
        }
    
    def create_budget(self, monthly_income: float) -> Dict:
        """Create a balanced budget"""
        template = self.templates.get(self.country, self.templates["global"])
        
        needs = monthly_income * (template["needs_percentage"] / 100)
        wants = monthly_income * (template["wants_percentage"] / 100)
        savings = monthly_income * (template["savings_percentage"] / 100)
        
        return {
            "monthly_income": monthly_income,
            "needs": round(needs, 2),
            "wants": round(wants, 2),
            "savings": round(savings, 2),
            "percentages": template,
            "budget_rule": f"{template['needs_percentage']}/{template['wants_percentage']}/{template['savings_percentage']}"
        }
    
    def analyze_expenses(self, 
                        income: float, 
                        expenses: Dict[str, float]) -> Dict:
        """Analyze current spending vs budget"""
        total_expenses = sum(expenses.values())
        savings = income - total_expenses
        savings_rate = (savings / income) * 100 if income > 0 else 0
        
        # Categorize expenses
        categories = {
            "essential": ["rent", "food", "utilities", "transport", "health"],
            "discretionary": ["entertainment", "dining", "shopping", "travel"]
        }
        
        essential_total = 0
        discretionary_total = 0
        
        for category, amount in expenses.items():
            cat_lower = category.lower()
            if any(keyword in cat_lower for keyword in categories["essential"]):
                essential_total += amount
            else:
                discretionary_total += amount
        
        return {
            "income": income,
            "total_expenses": total_expenses,
            "savings": savings,
            "savings_rate": round(savings_rate, 1),
            "essential_spending": round(essential_total, 2),
            "discretionary_spending": round(discretionary_total, 2),
            "spending_breakdown": {
                "essential_pct": round((essential_total / total_expenses) * 100, 1) if total_expenses > 0 else 0,
                "discretionary_pct": round((discretionary_total / total_expenses) * 100, 1) if total_expenses > 0 else 0
            }
        }

class FinancialEducator:
    """Simple financial education content"""
    
    def __init__(self, country="global"):
        self.country = country
    
    def get_lessons(self) -> List[Dict]:
        """Get basic financial lessons"""
        lessons = [
            {
                "id": 1,
                "title": "Budgeting Basics",
                "description": "Learn to create and stick to a budget",
                "duration": "15 minutes",
                "topics": ["Income vs Expenses", "50/30/20 Rule", "Tracking Spending"],
                "country_tip": self._get_country_tip("budgeting")
            },
            {
                "id": 2,
                "title": "Emergency Fund",
                "description": "Why you need savings for emergencies",
                "duration": "10 minutes",
                "topics": ["How much to save", "Where to keep it", "When to use it"],
                "country_tip": self._get_country_tip("emergency")
            },
            {
                "id": 3,
                "title": "Understanding Debt",
                "description": "Good debt vs bad debt and how to manage it",
                "duration": "20 minutes",
                "topics": ["Interest Rates", "Payoff Strategies", "Debt Snowball Method"],
                "country_tip": self._get_country_tip("debt")
            },
            {
                "id": 4,
                "title": "Simple Investing",
                "description": "Start investing with small amounts",
                "duration": "25 minutes",
                "topics": ["Compound Interest", "Risk vs Return", "Diversification"],
                "country_tip": self._get_country_tip("investing")
            }
        ]
        
        return lessons
    
    def _get_country_tip(self, topic: str) -> str:
        """Get country-specific financial tip"""
        tips = {
            "pakistan": {
                "budgeting": "Include family obligations in your budget",
                "emergency": "Aim for 6 months due to job market volatility",
                "debt": "Avoid high-interest informal loans",
                "investing": "Start with National Savings Schemes for safety"
            },
            "italy": {
                "budgeting": "Factor in healthcare costs differently than in Pakistan",
                "emergency": "3 months is sufficient due to social safety nets",
                "debt": "Student loans have special conditions in Italy",
                "investing": "Consider BTP bonds for government-backed returns"
            }
        }
        
        return tips.get(self.country, {}).get(topic, "Start with basic principles")

class FinancialDashboard:
    """Simple text-based dashboard"""
    
    @staticmethod
    def display_summary(user_data: Dict):
        """Display financial summary"""
        print("\n" + "="*50)
        print("FINANCIAL HEALTH DASHBOARD")
        print("="*50)
        
        if "emergency_fund" in user_data:
            ef = user_data["emergency_fund"]
            print(f"\n🛡️  Emergency Fund:")
            print(f"   Target: {ef['target_months']} months (${ef['target_amount']:,.2f})")
        
        if "savings_goal" in user_data:
            sg = user_data["savings_goal"]
            print(f"\n🎯 Savings Goal:")
            print(f"   Months needed: {sg['months_needed']}")
            print(f"   Years needed: {sg['years_needed']}")
        
        if "budget" in user_data:
            budget = user_data["budget"]
            print(f"\n💰 Monthly Budget ({budget['budget_rule']} Rule):")
            print(f"   Needs: ${budget['needs']:,.2f}")
            print(f"   Wants: ${budget['wants']:,.2f}")
            print(f"   Savings: ${budget['savings']:,.2f}")
        
        if "debt" in user_data:
            debt = user_data["debt"]
            print(f"\n💳 Debt Payoff:")
            print(f"   Months to payoff: {debt['months_to_payoff']}")
            print(f"   Total interest: ${debt['total_interest']:,.2f}")
        
        print("\n" + "="*50)

def demonstrate_pakistani_scenario():
    """Show Pakistani family example"""
    print("\n🇵🇰 PAKISTANI FAMILY SCENARIO")
    print("-" * 30)
    
    # Setup calculators
    calculator = FinanceCalculator("pakistan")
    budget_planner = BudgetPlanner("pakistan")
    educator = FinancialEducator("pakistan")
    
    # Monthly income: 80,000 PKR
    monthly_income = 80000
    monthly_expenses = 60000
    
    print(f"\nMonthly Income: PKR {monthly_income:,}")
    print(f"Monthly Expenses: PKR {monthly_expenses:,}")
    
    # Emergency fund calculation
    emergency_fund = calculator.calculate_emergency_fund(monthly_expenses)
    print(f"\nEmergency Fund Target: {emergency_fund['target_months']} months")
    print(f"Amount needed: PKR {emergency_fund['target_amount']:,}")
    
    # Budget planning
    budget = budget_planner.create_budget(monthly_income)
    print(f"\nRecommended Budget ({budget['budget_rule']} Rule):")
    print(f"  Needs (50%): PKR {budget['needs']:,}")
    print(f"  Wants (30%): PKR {budget['wants']:,}")
    print(f"  Savings (20%): PKR {budget['savings']:,}")
    
    # Savings goal: House down payment (2,000,000 PKR)
    print(f"\n🏠 Saving for House Down Payment (PKR 2,000,000):")
    savings_goal = calculator.calculate_savings_goal(
        target_amount=2000000,
        monthly_saving=20000,
        current_savings=150000
    )
    print(f"  Current savings: PKR 150,000")
    print(f"  Monthly saving: PKR 20,000")
    print(f"  Time to goal: {savings_goal['years_needed']} years")
    
    # Financial lessons
    print(f"\n📚 Recommended First Lesson:")
    lessons = educator.get_lessons()
    first_lesson = lessons[0]
    print(f"  {first_lesson['title']}")
    print(f"  Tip: {first_lesson['country_tip']}")
    
    return {
        "emergency_fund": emergency_fund,
        "budget": budget,
        "savings_goal": savings_goal
    }

def demonstrate_italian_scenario():
    """Show Italian student example"""
    print("\n\n🇮🇹 ITALIAN STUDENT SCENARIO")
    print("-" * 30)
    
    calculator = FinanceCalculator("italy")
    budget_planner = BudgetPlanner("italy")
    educator = FinancialEducator("italy")
    
    # Student budget
    monthly_income = 800  # EUR from part-time + support
    monthly_expenses = 700
    
    print(f"\nMonthly Income: €{monthly_income:,}")
    print(f"Monthly Expenses: €{monthly_expenses:,}")
    
    # Emergency fund
    emergency_fund = calculator.calculate_emergency_fund(monthly_expenses)
    print(f"\nEmergency Fund: {emergency_fund['target_months']} months")
    print(f"Amount needed: €{emergency_fund['target_amount']:,}")
    
    # Budget
    budget = budget_planner.create_budget(monthly_income)
    print(f"\nStudent Budget ({budget['budget_rule']} Rule):")
    print(f"  Needs (40%): €{budget['needs']:,}")
    print(f"  Wants (30%): €{budget['wants']:,}")
    print(f"  Savings (30%): €{budget['savings']:,}")
    
    # Saving for master's degree
    print(f"\n🎓 Saving for Master's Degree (€15,000):")
    savings_goal = calculator.calculate_savings_goal(
        target_amount=15000,
        monthly_saving=200,
        current_savings=3000
    )
    print(f"  Current savings: €3,000")
    print(f"  Monthly saving: €200")
    print(f"  Time to goal: {savings_goal['years_needed']} years")
    
    # Compound interest example
    print(f"\n📈 Compound Interest Example:")
    investment = calculator.calculate_compound_interest(
        principal=1000,
        monthly_contribution=100,
        years=10,
        annual_return=0.07
    )
    print(f"  Start: €1,000 + €100/month for 10 years")
    print(f"  Result: €{investment['future_value']:,.2f}")
    print(f"  Interest earned: €{investment['interest_earned']:,.2f}")
    
    return {
        "emergency_fund": emergency_fund,
        "budget": budget,
        "savings_goal": savings_goal,
        "investment": investment
    }

def main():
    """Main demonstration function"""
    print("="*60)
    print("FinLit: Personal Finance Education Tool")
    print("Cattolica University Application Project")
    print("="*60)
    print("\nThis tool demonstrates basic financial calculations")
    print("with cultural awareness for Pakistan and Italy.")
    
    # Run demonstrations
    pakistan_data = demonstrate_pakistani_scenario()
    italy_data = demonstrate_italian_scenario()
    
    # Show dashboard summary
    print("\n" + "="*60)
    print("FINANCIAL DASHBOARD SUMMARY")
    print("="*60)
    
    dashboard = FinancialDashboard()
    dashboard.display_summary(pakistan_data)
    
    # Export sample data
    sample_data = {
        "project": "FinLit Finance Tool",
        "author": "Ahmed Raza",
        "purpose": "Cattolica University Application",
        "demonstrations": {
            "pakistan_scenario": pakistan_data,
            "italy_scenario": italy_data
        },
        "features": [
            "Emergency fund calculator",
            "Budget planner",
            "Savings goal tracker",
            "Debt payoff calculator",
            "Compound interest calculator",
            "Country-specific financial rules"
        ]
    }
    
    # Save to file
    with open("finlit_demo.json", "w") as f:
        json.dump(sample_data, f, indent=2)
    
    print(f"\n✅ Demonstration complete!")
    print(f"📁 Data saved to: finlit_demo.json")
    print(f"\nKey Learning Points:")
    print("  1. Financial needs vary by country")
    print("  2. Simple math can solve complex problems")
    print("  3. Technology makes finance education accessible")
    print("\n" + "="*60)

if __name__ == "__main__":
    main()
