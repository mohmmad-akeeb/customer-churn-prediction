#!/usr/bin/env python3
"""
Inspect the model pipeline to understand its structure
"""
import joblib

# Load the model
model = joblib.load('best_model_pipeline.pkl')

print("="*60)
print("MODEL PIPELINE INSPECTION")
print("="*60)

# Check if it's a pipeline
if hasattr(model, 'steps'):
    print("\nThis is a Pipeline with the following steps:")
    for i, (name, step) in enumerate(model.steps):
        print(f"\n  Step {i+1}: {name}")
        print(f"    Type: {type(step).__name__}")
        print(f"    Module: {type(step).__module__}")
        
        # Check if it's the final estimator
        if i == len(model.steps) - 1:
            print(f"\n  Final Estimator Details:")
            print(f"    Class: {step.__class__.__name__}")
            
            # Check for specific attributes
            if hasattr(step, 'estimators_'):
                print(f"    Number of estimators: {len(step.estimators_)}")
            if hasattr(step, 'n_estimators'):
                print(f"    n_estimators: {step.n_estimators}")
            if hasattr(step, 'max_depth'):
                print(f"    max_depth: {step.max_depth}")
            if hasattr(step, 'min_samples_leaf'):
                print(f"    min_samples_leaf: {step.min_samples_leaf}")
                
else:
    print(f"\nModel type: {type(model).__name__}")
    print(f"Module: {type(model).__module__}")

# Check predict_proba method
print("\n" + "="*60)
print("PROBABILITY PREDICTION CAPABILITY")
print("="*60)

if hasattr(model, 'predict_proba'):
    print("\n✓ Model has predict_proba method")
    
    # Check if final estimator has predict_proba
    if hasattr(model, 'steps'):
        final_estimator = model.steps[-1][1]
        print(f"✓ Final estimator ({final_estimator.__class__.__name__}) has predict_proba: {hasattr(final_estimator, 'predict_proba')}")
else:
    print("\n✗ Model does NOT have predict_proba method")

print("\n" + "="*60)
