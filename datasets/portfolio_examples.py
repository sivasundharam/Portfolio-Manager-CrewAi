from dotenv import load_dotenv
load_dotenv()

from langsmith import Client

client = Client()

dataset_name = "Portfolio Manager Benchmark Dataset"

examples = [
    # 1. Profitable tech portfolio (baseline)
    {
        "inputs": {
            "portfolio": {
                "owner": "John Doe",
                "date": "2025-08-23",
                "holdings": [
                    {"ticker": "AAPL", "quantity": 50, "purchase_price": 150.0, "current_price": 175.2},
                    {"ticker": "TSLA", "quantity": 20, "purchase_price": 600.0, "current_price": 680.5},
                ]
            }
        },
        "outputs": {
            "analysis_report": {
                "summary": {
                    "holdings": {
                        "AAPL": {
                            "quantity": 50,
                            "purchase_price": 150.0,
                            "current_price": "≈ 175.2 (should match input)",
                            "gain_loss": "Correctly computed (≈ 1250 USD).",
                            "percentage": "≈ 16.7% gain."
                        },
                        "TSLA": {
                            "quantity": 20,
                            "purchase_price": 600.0,
                            "current_price": "≈ 680.5 (should match input)",
                            "gain_loss": "Correctly computed (≈ 1610 USD).",
                            "percentage": "≈ 13.4% gain."
                        },
                    },
                    "total_value": "Correct sum of holdings current_value.",
                    "total_gain_loss": "Correct sum of individual gains.",
                    "gain_loss_percentage": "Correct % relative to total cost basis."
                },
                "risk_assessment": {
                    "diversification": "Low – only two tech holdings.",
                    "risk_level": "Moderate to High (sector concentration)."
                },
                "recommendations": {
                    "asset_allocation": "Suggest adding healthcare/consumer staples for balance.",
                    "risk_tolerance": "If risk-averse, reduce concentration in tech."
                },
                "market_insights": {
                    "trends": "Commentary on tech volatility is acceptable.",
                    "economic_indicators": "Reasonable mention of interest rate effects."
                },
                "financial_concepts": {
                    "gain_loss": "Should explain gain/loss clearly.",
                    "diversification": "Should explain diversification clearly."
                }
            }
        }
    },

    # 2. Major loss
    {
        "inputs": {
            "portfolio": {
                "owner": "Jane Smith",
                "date": "2025-08-23",
                "holdings": [
                    {"ticker": "NFLX", "quantity": 40, "purchase_price": 700.0, "current_price": 400.0},
                ]
            }
        },
        "outputs": {
            "analysis_report": {
                "summary": {
                    "holdings": {
                        "NFLX": {
                            "quantity": 40,
                            "purchase_price": 700.0,
                            "current_price": "≈ 400.0 (should match input)",
                            "gain_loss": "Correctly computed (≈ -12,000 USD).",
                            "percentage": "≈ -43% loss."
                        }
                    },
                    "total_value": "Correct (≈ 16,000 USD).",
                    "total_gain_loss": "Correct (≈ -12,000 USD).",
                    "gain_loss_percentage": "Correct (≈ -43%)."
                },
                "risk_assessment": {
                    "concentration": "Single stock = very high risk.",
                    "risk_level": "High – portfolio vulnerable."
                },
                "recommendations": {
                    "asset_allocation": "Suggest diversifying across multiple sectors.",
                    "risk_tolerance": "If risk-averse, reduce exposure to single stock."
                },
                "market_insights": {
                    "trends": "Optional commentary on streaming sector slowdown.",
                    "economic_indicators": "Reasonable mention of competition/regulation."
                },
                "financial_concepts": {
                    "gain_loss": "Should explain clearly.",
                    "diversification": "Should explain why single-stock portfolios are risky."
                }
            }
        }
    },

    # 3. Highly diversified
    {
        "inputs": {
            "portfolio": {
                "owner": "Family Trust",
                "date": "2025-08-23",
                "holdings": [
                    {"ticker": "JNJ", "quantity": 100, "purchase_price": 160.0, "current_price": 170.0},
                    {"ticker": "PG", "quantity": 200, "purchase_price": 135.0, "current_price": 140.0},
                    {"ticker": "XOM", "quantity": 150, "purchase_price": 90.0, "current_price": 95.0},
                    {"ticker": "AAPL", "quantity": 80, "purchase_price": 150.0, "current_price": 175.0},
                ]
            }
        },
        "outputs": {
            "analysis_report": {
                "summary": {
                    "total_value": "Should correctly sum all holdings.",
                    "total_gain_loss": "Should sum gains from all holdings.",
                    "gain_loss_percentage": "Should compute overall % gain correctly.",
                },
                "risk_assessment": {
                    "diversification": "High – multiple sectors covered.",
                    "risk_level": "Balanced risk exposure."
                },
                "recommendations": {
                    "asset_allocation": "Maintain balance or consider small fixed-income allocation.",
                    "risk_tolerance": "Tailored guidance is acceptable."
                },
                "market_insights": {
                    "trends": "Sector commentary (tech, staples, energy) acceptable.",
                    "economic_indicators": "Interest rates and inflation may affect staples/energy."
                },
                "financial_concepts": {
                    "diversification": "Explain concept clearly.",
                    "gain_loss": "Explain clearly."
                }
            }
        }
    },

    # 4. Multi-owner
    {
        "inputs": {
            "portfolio": {
                "owner": "Joint Account (Alice & Bob)",
                "date": "2025-08-23",
                "holdings": [
                    {"ticker": "MSFT", "quantity": 30, "purchase_price": 320.0, "current_price": 340.0},
                    {"ticker": "AMZN", "quantity": 25, "purchase_price": 3000.0, "current_price": 3300.0},
                ]
            }
        },
        "outputs": {
            "analysis_report": {
                "summary": {
                    "total_value": "Correct sum of holdings.",
                    "total_gain_loss": "Correct (≈ 750 + 7500).",
                    "gain_loss_percentage": "Correct % relative to cost basis."
                },
                "risk_assessment": {
                    "ownership": "Multiple owners.",
                    "diversification": "Low – only 2 holdings, both tech/consumer internet.",
                },
                "recommendations": {
                    "asset_allocation": "Suggest more sectors or ETFs.",
                    "risk_tolerance": "Guidance depending on joint goals."
                },
                "market_insights": {
                    "trends": "Commentary on software/cloud and e-commerce acceptable.",
                    "economic_indicators": "Interest rate and consumer spending impacts."
                },
                "financial_concepts": {
                    "gain_loss": "Should explain clearly.",
                    "diversification": "Should explain clearly."
                }
            }
        }
    },

    # 5. Foreign currency
    {
        "inputs": {
            "portfolio": {
                "owner": "Global Investor",
                "date": "2025-08-23",
                "holdings": [
                    {"ticker": "BABA", "quantity": 100, "purchase_price": 200.0, "current_price": 220.0, "currency": "HKD"},
                    {"ticker": "SAP", "quantity": 50, "purchase_price": 120.0, "current_price": 130.0, "currency": "EUR"},
                ]
            }
        },
        "outputs": {
            "analysis_report": {
                "summary": {
                    "holdings": {
                        "BABA": {
                            "quantity": 100,
                            "purchase_price": 200.0,
                            "current_price": "≈ 220 HKD",
                            "gain_loss": "Correctly computed (≈ 2000 HKD).",
                            "percentage": "≈ 10% gain."
                        },
                        "SAP": {
                            "quantity": 50,
                            "purchase_price": 120.0,
                            "current_price": "≈ 130 EUR",
                            "gain_loss": "Correctly computed (≈ 500 EUR).",
                            "percentage": "≈ 4% gain."
                        }
                    },
                    "total_value": "Correct combined HKD + EUR (no FX conversion assumed).",
                    "total_gain_loss": "Correct combined gain.",
                    "gain_loss_percentage": "Correct overall % relative to cost basis."
                },
                "risk_assessment": {
                    "currency_risk": "Present – FX exposure.",
                    "diversification": "Moderate – two holdings, different regions.",
                },
                "recommendations": {
                    "asset_allocation": "Suggest FX hedging or USD exposure.",
                    "risk_tolerance": "If aggressive, FX risk may be acceptable."
                },
                "market_insights": {
                    "trends": "China tech & EU software commentary acceptable.",
                    "economic_indicators": "FX rates, inflation, ECB/China policy effects."
                },
                "financial_concepts": {
                    "gain_loss": "Should explain clearly.",
                    "diversification": "Should explain clearly.",
                    "currency_risk": "Should explain FX exposure concept."
                }
            }
        }
    }
]

# Register dataset
if not client.has_dataset(dataset_name=dataset_name):
    dataset = client.create_dataset(dataset_name=dataset_name)

    client.create_examples(
        inputs=[ex["inputs"] for ex in examples],
        outputs=[ex["outputs"] for ex in examples],
        dataset_id=dataset.id,
    )

print(f" Dataset '{dataset_name}' registered with {len(examples)} examples.")
