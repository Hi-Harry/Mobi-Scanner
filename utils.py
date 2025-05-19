def calculate_spam_likelihood(phone_number, Contact, SpamReport):
    total_reports = SpamReport.query.filter_by(phone_number=phone_number).count()
    total_entries = Contact.query.filter_by(phone_number=phone_number).count()
    if total_entries == 0:
        return "0%"
    return f"{int((total_reports / total_entries) * 100)}%"