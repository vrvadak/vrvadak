st.markdown("""
    <style>
    /* Prioritization Styles */
    .priority-high {
        color: #dc3545; /* Red for high priority */
        font-weight: bold;
    }

    .priority-medium {
        color: #ffc107; /* Yellow for medium priority */
        font-weight: bold;
    }

    .priority-low {
        color: #28a745; /* Green for low priority */
        font-weight: bold;
    }

    /* Due Date Styles */
    .due-date {
        color: #007bff; /* Blue color for due dates */
        font-style: italic;
    }

    /* Tag Styles */
    .tag {
        display: inline-block;
        background-color: #e2e6ea; /* Light gray background for tags */
        border-radius: 4px; /* Rounded corners for tags */
        padding: 4px 8px; /* Padding inside tags */
        margin: 2px; /* Space between tags */
        font-size: 12px; /* Smaller font size for tags */
        color: #495057; /* Darker text color for tags */
    }

    /* Comments Section */
    .comments-section {
        border-top: 1px solid #ddd; /* Light border for comments section */
        padding-top: 10px; /* Padding above comments section */
    }
    </style>
""", unsafe_allow_html=True)
