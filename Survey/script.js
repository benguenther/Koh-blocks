let code
let date
let sex
let gender
let age
let english
let handedness

let q1
let q2
let q3
let q4
let q5
let q6
let q7
let q8
let q9
let q10
let q11
let q12

let parents_hand, sib_female, sib_male, female_l, male_l, primary_eye;

document.getElementById("submit").onclick = function(){
    code = document.getElementById("code_num").value;
    date = document.getElementById("date").value;
    sex = document.getElementById("sex").value;
    gender = document.getElementById("gender").value;
    age = document.getElementById("age").value;
    english = document.getElementById("eng").value;
    handedness = document.getElementById("handedness").value;

    q1 = document.getElementById("q1").value;
    q2 = document.getElementById("q2").value;
    q3 = document.getElementById("q3").value;
    q4 = document.getElementById("q4").value;
    q5 = document.getElementById("q5").value;
    q6 = document.getElementById("q6").value;
    q7 = document.getElementById("q7").value;
    q8 = document.getElementById("q8").value;
    q9 = document.getElementById("q9").value;
    q10 = document.getElementById("q10").value;
    q11 = document.getElementById("q11").value;
    q12 = document.getElementById("q12").value;

    parents_hand = document.getElementById("parents_hand").value;
    sib_female = document.getElementById("sib_female").value;
    sib_male = document.getElementById("sib_male").value;
    female_l = document.getElementById("female_l").value;
    male_l = document.getElementById("male_l").value;
    primary_eye = document.getElementById("primary_eye").value;

    const rows = [
        ["code", "date", "sex", "gender", "age", "english", "handedness", "q1", "q2", "q3", "q4", "q5", "q6", "q7", "q8", "q9", "q10", "q11", "q12", "parents_hand", "sib_female", "sib_male", "female_l", "male_l", "primary_eye"],
        [code, date, sex, gender, age, english, handedness, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12, parents_hand, sib_female, sib_male, female_l, male_l, primary_eye]   
    ];

    let filename = "info_"+code;

    let csvContent = rows.map(e => e.join(",")).join("\n");

    const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
    const url = URL.createObjectURL(blob);

    const link = document.createElement("a");
    link.setAttribute("href", url);
    link.setAttribute("download", filename);  // fixed filename
    link.click();
}