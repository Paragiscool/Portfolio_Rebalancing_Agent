import numpy as np
import cvxpy as cp
import pandas as pd


class PortfolioOptimiser:
    """Constrained optimization engine using CVXPY."""

    def __init__(self, constraint_manager):
        self.constraint_manager = constraint_manager

    def optimize(
        self,
        current_weights: np.ndarray,
        target_weights: np.ndarray,
        covariance_matrix: np.ndarray,
    ) -> np.ndarray:
        """
        Solves the quadratic programming problem to minimize tracking error
        subject to turnover and long-only constraints.

        :param current_weights: Array of current portfolio weights
        :param target_weights: Array of target portfolio weights
        :param covariance_matrix: Covariance matrix of asset returns
        :return: Array of optimized weights
        """
        n_assets = len(current_weights)

        # Variable: the new portfolio weights
        w = cp.Variable(n_assets)

        # Objective: minimize (w - w_target)^T * Cov * (w - w_target)
        # To make it strictly PSD for CVXPY, we can use cp.quad_form
        # CVXPY requires the matrix to be PSD. We add a tiny value to diagonal if needed,
        # but the covariance matrix from our generator is PSD.
        tracking_error = cp.quad_form(w - target_weights, covariance_matrix)
        objective = cp.Minimize(tracking_error)

        # Constraints
        constraints = [cp.sum(w) == 1.0, w >= 0]  # Fully invested  # Long only

        # Turnover limit constraint
        # Turnover = 0.5 * sum(|w - w_current|)
        max_turnover = self.constraint_manager.get_max_turnover()
        turnover = 0.5 * cp.norm(w - current_weights, 1)
        constraints.append(turnover <= max_turnover)

        # Formulate and solve the problem
        prob = cp.Problem(objective, constraints)

        # OSQP is fast for QP problems
        prob.solve(solver=cp.OSQP)

        if prob.status not in ["optimal", "optimal_inaccurate"]:
            # Fallback solver if OSQP fails
            prob.solve(solver=cp.ECOS)
            if prob.status not in ["optimal", "optimal_inaccurate"]:
                raise ValueError(
                    f"Optimizer failed to find an optimal solution. Status: {prob.status}"
                )

        # Ensure exact precision issues don't create tiny negative weights
        optimized_weights = np.maximum(w.value, 0)
        # Re-normalize to ensure exactly 1.0 sum
        optimized_weights = optimized_weights / np.sum(optimized_weights)

        return optimized_weights
