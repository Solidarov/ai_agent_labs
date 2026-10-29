# Prompt
```
Classify emails into one of these categories: [spam, important, personal].

Examples:
Email: "Get 80% off on luxury watches today! Click here to claim." -> spam
Email: "Hey, are we still meeting for coffee this Sunday?" -> personal
Email: "Urgent: The Q3 Budget Review meeting has been rescheduled to 2 PM today." -> important

Email: "Hey! Yeah, I got that invoice (#84930 or whatever). I can pay it by tomorrow, but wait... why are we paying this again? Thought you already settled it last week. Let me know before I send the money."
```

# Result
```
Email: "Hey! Yeah, I got that invoice (#84930 or whatever). I can pay it by tomorrow, but wait... why are we paying this again? Thought you already settled it last week. Let me know before I send the money." -> important

(Why? Even though it starts casually ("Hey!"), it discusses a specific business invoice, payment deadlines, and money matters, which requires attention and action.)
```