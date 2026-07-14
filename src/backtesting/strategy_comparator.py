import os
from src.backtesting.backtest_engine import BacktestEngine
from src.backtesting.performance_analyser import PerformanceAnalyser

class StrategyComparator:
    def __init__(self, output_dir: str = "reports/backtests"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        
    def run_comparison(self):
        engine = BacktestEngine(initial_capital=100000.0, transaction_cost_bps=10.0)
        analyser = PerformanceAnalyser()
        
        target_weights = {"AAPL": 0.60, "GOOGL": 0.40}
        
        # Generate 1 year of synthetic data
        prices = engine.generate_synthetic_prices(["AAPL", "GOOGL"], days=252)
        
        # Run Strategies
        bnh_results = engine.run_backtest(prices, target_weights, strategy="buy_and_hold")
        agent_results = engine.run_backtest(prices, target_weights, strategy="threshold_rebalance", threshold=0.05)
        
        bnh_metrics = analyser.analyze(bnh_results)
        agent_metrics = analyser.analyze(agent_results)
        
        self._generate_report(bnh_metrics, agent_metrics)
        print(f"Backtest comparison report generated in {self.output_dir}/backtest_report.md")

    def _generate_report(self, bnh: dict, agent: dict):
        doc = "# Strategy Backtest Comparison\n\n"
        doc += "This report compares the autonomous Threshold-based Rebalancing Agent against a simple Buy & Hold strategy over a 1-year synthetic market simulation.\n\n"
        
        doc += "| Metric | Buy & Hold | Agent (Rebalanced) |\n"
        doc += "|---|---|---|\n"
        
        metrics = ["Total Return", "Annualized Return", "Annualized Vol", "Sharpe Ratio", "Max Drawdown", "Total Turnover"]
        
        for m in metrics:
            val_bnh = bnh.get(m, 0)
            val_agent = agent.get(m, 0)
            
            # Formatting
            if m in ["Total Turnover"]:
                val_bnh_str = f"${val_bnh:,.2f}"
                val_agent_str = f"${val_agent:,.2f}"
            elif m in ["Sharpe Ratio"]:
                val_bnh_str = f"{val_bnh:.2f}"
                val_agent_str = f"{val_agent:.2f}"
            else:
                val_bnh_str = f"{val_bnh:.2%}"
                val_agent_str = f"{val_agent:.2%}"
                
            doc += f"| {m} | {val_bnh_str} | {val_agent_str} |\n"
            
        doc += "\n## Conclusion\n"
        doc += "The Agent successfully executed rebalancing trades to maintain target drift constraints."
        
        filepath = os.path.join(self.output_dir, "backtest_report.md")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(doc)

if __name__ == "__main__":
    comparator = StrategyComparator()
    comparator.run_comparison()
