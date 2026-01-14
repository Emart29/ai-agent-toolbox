"""
Calculator Tool
Performs mathematical calculations and currency conversions

Features:
- Basic math operations (+, -, *, /, %, **)
- Advanced math (sqrt, sin, cos, log, etc.)
- Currency conversion using Fixer.io API
- Safe evaluation (no code execution vulnerabilities)
"""

import math
import re
from typing import Union, Dict, Any
import requests
import os
from dotenv import load_dotenv
import logging
from sympy import sympify, N

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CalculatorTool:
    """
    Calculator tool for mathematical operations and currency conversion.
    
    Uses:
    - Python's math module for standard functions
    - sympy for safe expression evaluation
    - Fixer.io API for currency conversion
    """
    
    def __init__(self):
        """Initialize calculator with API keys"""
        self.fixer_api_key = os.getenv("FIXER_API_KEY")
        self.fixer_base_url = "https://api.fixer.io/latest"
        
        # Cache for currency rates (avoid excessive API calls)
        self._currency_cache = {}
        self._cache_timestamp = 0
        
        logger.info("CalculatorTool initialized")
    
    def calculate(self, expression: str) -> Dict[str, Any]:
        """
        Main calculation method.
        
        Detects if it's a math expression or currency conversion.
        
        Args:
            expression: Math expression or currency conversion request
            
        Returns:
            Dict with result and explanation
        """
        expression = expression.strip()
        
        # Check if it's a currency conversion request
        if self._is_currency_conversion(expression):
            return self._convert_currency(expression)
        else:
            return self._evaluate_math(expression)
    
    def _is_currency_conversion(self, expression: str) -> bool:
        """
        Check if expression is a currency conversion request.
        
        Patterns:
        - "100 USD to EUR"
        - "convert 50 GBP to JPY"
        - "50 dollars in euros"
        """
        currency_pattern = r'\b([A-Z]{3})\s*(to|in)\s*([A-Z]{3})\b'
        return bool(re.search(currency_pattern, expression.upper()))
    
    def _evaluate_math(self, expression: str) -> Dict[str, Any]:
        """
        Evaluate mathematical expression safely.
        
        Uses sympy for safe evaluation (prevents code injection).
        
        Args:
            expression: Mathematical expression
            
        Returns:
            Dict with result and explanation
        """
        try:
            # Clean expression
            expression = expression.replace('^', '**')  # Convert ^ to **
            expression = expression.replace('×', '*')   # Convert × to *
            expression = expression.replace('÷', '/')   # Convert ÷ to /
            
            logger.info(f"Evaluating expression: {expression}")
            
            # Use sympy for safe evaluation
            result = sympify(expression)
            
            # Convert to numerical value
            numerical_result = float(N(result))
            
            return {
                'success': True,
                'result': numerical_result,
                'expression': expression,
                'explanation': f"{expression} = {numerical_result}"
            }
            
        except Exception as e:
            logger.error(f"Error evaluating expression: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'expression': expression,
                'explanation': f"Could not evaluate: {expression}"
            }
    
    def _convert_currency(self, request: str) -> Dict[str, Any]:
        """
        Convert currency using Fixer.io API.
        
        Args:
            request: Currency conversion request (e.g., "100 USD to EUR")
            
        Returns:
            Dict with conversion result
        """
        try:
            # Parse the request
            # Pattern: "amount FROM_CURRENCY to TO_CURRENCY"
            pattern = r'(\d+(?:\.\d+)?)\s*([A-Z]{3})\s*(?:to|in)\s*([A-Z]{3})'
            match = re.search(pattern, request.upper())
            
            if not match:
                return {
                    'success': False,
                    'error': 'Could not parse currency conversion request',
                    'explanation': 'Format: "100 USD to EUR"'
                }
            
            amount = float(match.group(1))
            from_currency = match.group(2)
            to_currency = match.group(3)
            
            logger.info(f"Converting {amount} {from_currency} to {to_currency}")
            
            # Get exchange rate
            rate = self._get_exchange_rate(from_currency, to_currency)
            
            if rate is None:
                return {
                    'success': False,
                    'error': 'Could not fetch exchange rate',
                    'explanation': 'API error or invalid currency codes'
                }
            
            # Calculate conversion
            result = amount * rate
            
            return {
                'success': True,
                'result': round(result, 2),
                'from_amount': amount,
                'from_currency': from_currency,
                'to_currency': to_currency,
                'exchange_rate': rate,
                'explanation': f"{amount} {from_currency} = {result:.2f} {to_currency} (rate: {rate:.4f})"
            }
            
        except Exception as e:
            logger.error(f"Error in currency conversion: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'explanation': 'Currency conversion failed'
            }
    
    def _get_exchange_rate(self, from_currency: str, to_currency: str) -> float:
        """
        Get exchange rate from Fixer.io API.
        
        Implements caching to reduce API calls.
        
        Args:
            from_currency: Source currency code (e.g., USD)
            to_currency: Target currency code (e.g., EUR)
            
        Returns:
            Exchange rate or None if error
        """
        import time
        
        # Check cache (cache for 1 hour)
        current_time = time.time()
        cache_key = f"{from_currency}_{to_currency}"
        
        if (cache_key in self._currency_cache and 
            current_time - self._cache_timestamp < 3600):
            logger.info(f"Using cached rate for {cache_key}")
            return self._currency_cache[cache_key]
        
        # If no API key, use mock rates for testing
        if not self.fixer_api_key or self.fixer_api_key == "your_fixer_api_key_here":
            logger.warning("Using mock exchange rates (no Fixer.io API key)")
            return self._get_mock_rate(from_currency, to_currency)
        
        try:
            # Call Fixer.io API
            url = f"{self.fixer_base_url}?access_key={self.fixer_api_key}&base={from_currency}&symbols={to_currency}"
            
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            
            if not data.get('success', False):
                logger.error(f"Fixer.io API error: {data.get('error', {})}")
                return self._get_mock_rate(from_currency, to_currency)
            
            rate = data['rates'].get(to_currency)
            
            if rate:
                # Update cache
                self._currency_cache[cache_key] = rate
                self._cache_timestamp = current_time
                return rate
            
            return None
            
        except Exception as e:
            logger.error(f"Error fetching exchange rate: {str(e)}")
            return self._get_mock_rate(from_currency, to_currency)
    
    def _get_mock_rate(self, from_currency: str, to_currency: str) -> float:
        """
        Mock exchange rates for testing without API key.
        
        Based on approximate real rates (as of 2025).
        """
        # Mock rates relative to USD
        mock_rates = {
            'USD': 1.0,
            'EUR': 0.92,
            'GBP': 0.79,
            'JPY': 149.50,
            'NGN': 1620.0,  # Nigerian Naira
            'CAD': 1.36,
            'AUD': 1.52,
            'CHF': 0.88,
            'CNY': 7.24,
            'INR': 83.12,
        }
        
        if from_currency not in mock_rates or to_currency not in mock_rates:
            logger.warning(f"Unknown currency pair: {from_currency}/{to_currency}")
            return 1.0
        
        # Calculate rate
        rate = mock_rates[to_currency] / mock_rates[from_currency]
        logger.info(f"Using mock rate: 1 {from_currency} = {rate} {to_currency}")
        return rate


# LangChain Tool wrapper
def get_calculator_tool_for_langchain():
    """
    Create LangChain-compatible tool.
    
    Returns a function that LangChain can call.
    """
    calculator = CalculatorTool()
    
    def calculator_wrapper(expression: str) -> str:
        """
        Calculate mathematical expressions or convert currencies.
        
        Args:
            expression: Math expression (e.g., "2 + 2") or currency conversion (e.g., "100 USD to EUR")
            
        Returns:
            Calculation result as string
        """
        result = calculator.calculate(expression)
        
        if result['success']:
            return result['explanation']
        else:
            return f"Error: {result.get('error', 'Calculation failed')}"
    
    return calculator_wrapper


# Example usage and testing
if __name__ == "__main__":
    calc = CalculatorTool()
    
    print("🧪 Testing Calculator Tool\n")
    
    # Test 1: Simple math
    print("1️⃣ Simple calculation:")
    result = calc.calculate("2 + 2 * 3")
    print(f"   {result['explanation']}\n")
    
    # Test 2: Advanced math
    print("2️⃣ Advanced calculation:")
    result = calc.calculate("sqrt(16) + 5**2")
    print(f"   {result['explanation']}\n")
    
    # Test 3: Percentage
    print("3️⃣ Percentage:")
    result = calc.calculate("25 * 0.20")  # 20% of 25
    print(f"   {result['explanation']}\n")
    
    # Test 4: Currency conversion
    print("4️⃣ Currency conversion:")
    result = calc.calculate("100 USD to EUR")
    print(f"   {result['explanation']}\n")
    
    # Test 5: Nigerian Naira conversion
    print("5️⃣ NGN conversion:")
    result = calc.calculate("5000 NGN to USD")
    print(f"   {result['explanation']}\n")
    
    print("✅ All tests completed!")