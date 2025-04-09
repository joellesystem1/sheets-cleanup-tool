import streamlit as st
import pandas as pd

def cleanup_csv(df):
    try:
        # Show data statistics before cleaning
        total_rows = len(df)
        
        # Find the submission status column (it might be named differently)
        status_columns = [col for col in df.columns if 'submit' in col.lower()]
        if not status_columns:
            st.error("Could not find a column containing submission status.")
            st.write("Available columns:", df.columns.tolist())
            return None, None
            
        column_name = status_columns[0]
        st.info(f"Using column: {column_name}")
        
        # Keep rows where:
        # 1. Status contains 'New Article' OR
        # 2. Status contains 'needs review'
        # BUT remove rows with 'Completed' or 'Submitted' (unless they have 'needs review')
        df_cleaned = df[
            (
                (df[column_name].str.contains('New Article|needs review', na=False, case=False)) |
                (df[column_name].str.contains('Submitted.*needs review', na=False, case=False))
            ) & 
            (~df[column_name].str.contains('Completed(?!.*needs review)', na=False, case=False))
        ]
        
        # Show statistics
        rows_removed = total_rows - len(df_cleaned)
        stats = {
            'Total Rows': total_rows,
            'Rows Kept (New Articles + Needs Review)': len(df_cleaned),
            'Other Rows Removed': rows_removed
        }
        return df_cleaned, stats
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.write("Available columns:", df.columns.tolist())  # Debug info
        return None, None

def main():
    st.title("Article Status Cleanup Tool")
    
    with st.expander("ℹ️ How to use this tool"):
        st.markdown("""
        1. Download your sheet as CSV from Google Sheets
        2. Upload the CSV file here
        3. Click 'Clean Data' to:
           - Keep 'New Article' rows
           - Keep rows marked as 'needs review'
           - Remove other 'Completed' and 'Submitted' rows
        4. Download the cleaned CSV
        """)
    
    uploaded_file = st.file_uploader("Upload your CSV file", type=['csv'])
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.success("✅ File uploaded successfully!")
            
            # Show original data statistics
            st.subheader("Original Data Preview:")
            st.dataframe(df.head())
            
            # Find submission status column
            status_columns = [col for col in df.columns if 'submit' in col.lower()]
            if status_columns:
                column_name = status_columns[0]
                status_counts = df[column_name].value_counts()
                st.write(f"Current Status Counts for column '{column_name}':")
                st.write(status_counts)
            
            if st.button("Clean Data"):
                with st.spinner("Cleaning data..."):
                    cleaned_df, stats = cleanup_csv(df)
                    
                    if cleaned_df is not None:
                        # Show statistics
                        st.success("Data cleaned successfully!")
                        st.write("Statistics:")
                        for key, value in stats.items():
                            st.write(f"- {key}: {value}")
                        
                        # Show preview of cleaned data
                        st.subheader("Preview of cleaned data (New Articles + Needs Review):")
                        st.dataframe(cleaned_df.head())
                        
                        # Provide download button
                        csv = cleaned_df.to_csv(index=False)
                        st.download_button(
                            label="Download cleaned CSV",
                            data=csv,
                            file_name="articles_to_review.csv",
                            mime="text/csv"
                        )
                        st.balloons()
            
            # Show column names at the bottom in an expander
            with st.expander("📋 View All Available Columns"):
                st.write("These are all the columns in your CSV file:")
                st.write(df.columns.tolist())
        
        except Exception as e:
            st.error(f"Error reading the file: {str(e)}")
            st.write("Error details:", str(e))

if __name__ == "__main__":
    main() 