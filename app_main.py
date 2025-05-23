import streamlit as st
import pandas as pd
import openpyxl
import io

# Προστασία με κωδικό και αποδοχή όρων
def password_gate():
    password = st.text_input("🔒 Εισάγετε τον κωδικό πρόσβασης:", type="password")
    if password != "katanomi2025":
        st.warning("Ο κωδικός είναι λανθασμένος.")
        st.stop()

    st.markdown("⚠️ **Νομική Επισήμανση**")
    st.markdown("""
    Απαγορεύεται η χρήση της εφαρμογής χωρίς ρητή γραπτή άδεια από την δημιουργό.  
    Όλα τα πνευματικά δικαιώματα ανήκουν στη **Γιαννίτσαρου Παναγιώτα**.
    """)

    agree = st.checkbox("✅ Αποδέχομαι τους παραπάνω όρους χρήσης.")
    if not agree:
        st.warning("Πρέπει να αποδεχτείτε τους όρους για να συνεχίσετε.")
        st.stop()

password_gate()

st.set_page_config(page_title="Κατανομή Μαθητών", layout="wide")

tab1, tab2, tab3, tab4 = st.tabs(["🔷 Εισαγωγή & Έμπνευση", "📋 Κατανομή", "📚 Συχνές Ερωτήσεις", "📬 Επικοινωνία"])

# TAB 1
with tab1:
    subtab1, subtab2 = st.tabs(["🎯 Σκοπός Εφαρμογής", "🧭 Πηγή Έμπνευσης"])
    with subtab1:
        st.markdown("""
        Σκοπός της εφαρμογής είναι να στηρίξει τη **δίκαιη** και **παιδαγωγικά ισορροπημένη** κατανομή των μαθητών της Α’ Δημοτικού.

        Ως γονιός που διαπίστωσε αδικίες στην πράξη, ένιωσα την ευθύνη να προσφέρω ένα εργαλείο που να υπηρετεί τις αρχές της **ισότητας**, της **διαφάνειας** και της **παιδαγωγικής ευαισθησίας**.
        """)
    with subtab2:
        st.markdown("""
        Η εφαρμογή αυτή γεννήθηκε από μια εσωτερική ανάγκη: να διασφαλίσει τα δικαιώματα όλων των παιδιών...

        “No man is an island,<br>
        Entire of itself;<br>
        ...<br>
        It tolls for thee.”<br><br>
        — John Donne
        """, unsafe_allow_html=True)

    # λογότυπο κάτω δεξιά
    st.markdown("""
    <div style='text-align: right; padding-top: 2rem; padding-right: 0.5rem;'>
        <img src='final_logo_bottom_right.png' width='140'>
    </div>
    """, unsafe_allow_html=True)

# TAB 2
with tab2:
    st.header("📋 Κατανομή Μαθητών")
    uploaded_file = st.file_uploader("📂 Ανέβασε το αρχείο Excel με τους μαθητές", type=["xlsx"])

    if uploaded_file:
        df = pd.read_excel(uploaded_file)
        st.success("✅ Το αρχείο ανέβηκε και διαβάστηκε επιτυχώς.")
        st.dataframe(df)

        if st.button("🔘 Ξεκίνα την Κατανομή"):
            students = df.to_dict(orient="records")
            num_classes = max(1, len(students) // 25)
            classes = [[] for _ in range(num_classes)]

            assign_teacher_children(students, classes)
            assign_zoiroi_with_friends(students, classes)
            assign_special_students(students, classes)
            assign_language_weak(students, classes)
            assign_friend_pairs(students, classes)
            assign_remaining_students_without_friends(students, classes)

            st.success("✅ Η κατανομή ολοκληρώθηκε!")

            for i, cl in enumerate(classes):
                st.subheader(f"📘 Τμήμα {i + 1} ({len(cl)} μαθητές)")
                df_cl = pd.DataFrame(cl)
                st.dataframe(df_cl)

                boys = sum(1 for s in cl if s.get('gender') == 'Α')
                girls = sum(1 for s in cl if s.get('gender') == 'Θ')
                zoiroi = sum(1 for s in cl if s.get('zoiros'))
                teachers_kids = sum(1 for s in cl if s.get('teacher_child'))

                st.markdown(f"👦 Αγοριών: **{boys}**")
                st.markdown(f"👧 Κοριτσιών: **{girls}**")
                st.markdown(f"💥 Ζωηροί: **{zoiroi}**")
                st.markdown(f"🎓 Παιδιά εκπαιδευτικών: **{teachers_kids}**")

            result = []
            for i, cl in enumerate(classes):
                for student in cl:
                    student["Τμήμα"] = f"Τμήμα {i + 1}"
                    result.append(student)
            result_df = pd.DataFrame(result)

            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                result_df.to_excel(writer, index=False, sheet_name="Κατανομή")
            output.seek(0)

            st.download_button("📥 Κατέβασε Κατανομή σε Excel", data=output, file_name="katanomi.xlsx")

    st.markdown("""
    <div style='text-align: right; padding-top: 2rem; padding-right: 0.5rem;'>
        <img src='final_logo_bottom_right.png' width='140'>
    </div>
    """, unsafe_allow_html=True)

# TAB 3
with tab3:
    st.header("📚 Συχνές Ερωτήσεις (FAQ)")

    st.markdown("**Ποιο αρχείο χρειάζομαι;** Excel (.xlsx) με τις στήλες φύλου, ιδιαιτερότητας κ.λπ.")
    st.markdown("**Τι κάνει η εφαρμογή;** Κατανέμει μαθητές δίκαια, με βάση παιδαγωγικά κριτήρια.")
    st.markdown("**Ποια είναι τα στάδια;** Εκπαιδευτικοί → Ζωηροί → Ιδιαιτερότητες → Γλωσσική → Φίλοι → Υπόλοιποι.")
    st.markdown("**Παραδείγματα αρχείων:** [Παράδειγμα.xlsx](Παραδειγμα.xlsx) | [Πρότυπο.xlsx](Πρότυπο_Κατανομής%20κενό.xlsx)")

    st.markdown("""
    <div style='text-align: right; padding-top: 2rem; padding-right: 0.5rem;'>
        <img src='final_logo_bottom_right.png' width='140'>
    </div>
    """, unsafe_allow_html=True)

# TAB 4
with tab4:
    st.header("📬 Επικοινωνία")

    st.markdown("""
    📩 Email: yiannitsaroupanayiota.katanomi@gmail.com  
    🧑‍💻 Δημιουργός: Παναγιώτα Γιαννίτσαρου  
    ⚠️ Η εφαρμογή βρίσκεται σε πιλοτική λειτουργία.
    """)

    st.markdown("""
    <div style='text-align: right; padding-top: 2rem; padding-right: 0.5rem;'>
        <img src='final_logo_bottom_right.png' width='140'>
    </div>
    """, unsafe_allow_html=True)