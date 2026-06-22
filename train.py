import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

def main():
    columns = [
        'duration', 'protocol_type', 'service', 'flag', 'src_bytes', 'dst_bytes', 
        'land', 'wrong_fragment', 'urgent', 'hot', 'num_failed_logins', 'logged_in', 
        'num_compromised', 'root_shell', 'su_attempted', 'num_root', 'num_file_creations', 
        'num_shells', 'num_access_files', 'num_outbound_cmds', 'is_host_login', 
        'is_guest_login', 'count', 'srv_count', 'serror_rate', 'srv_serror_rate', 
        'rerror_rate', 'srv_rerror_rate', 'same_srv_rate', 'diff_srv_rate', 
        'srv_diff_host_rate', 'dst_host_count', 'dst_host_srv_count', 
        'dst_host_same_srv_rate', 'dst_host_diff_srv_rate', 'dst_host_same_src_port_rate', 
        'dst_host_srv_diff_host_rate', 'dst_host_serror_rate', 'dst_host_srv_serror_rate', 
        'dst_host_rerror_rate', 'dst_host_srv_rerror_rate', 'attack', 'level'
    ]
    
    print("📥 Loading NSL-KDD Training Dataset Data...")
    df = pd.read_csv("KDDTrain+.txt", header=None, names=columns)
    
    df = df.drop('level', axis=1)
    
    df['target'] = df['attack'].apply(lambda x: 0 if x == 'normal' else 1)
    df = df.drop('attack', axis=1)
    
    categorical_features = ['protocol_type', 'service', 'flag']
    df_encoded = pd.get_dummies(df, columns=categorical_features, drop_first=True)
    
    X = df_encoded.drop('target', axis=1)
    y = df_encoded['target']
    
    feature_names = list(X.columns)
    joblib.dump(feature_names, "model_features.pkl")
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("🛡️ Training AI Intrusion Classifier Engine...")
    model = RandomForestClassifier(n_estimators=100, max_depth=12, random_state=42)
    model.fit(X_train, y_train)
    
    preds = model.predict(X_test)
    print("\n📊 Validation Metrics Report:")
    print(classification_report(y_test, preds))
    
    joblib.dump(model, "nids_model.pkl")
    print("✅ Training complete. Assets saved successfully!")

if __name__ == "__main__":
    main()
