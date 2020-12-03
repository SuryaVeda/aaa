var si = document.getElementsByClassName('search_input');
var personalForm = document.getElementsByClassName('personal-form');
var degreeForm = document.getElementsByClassName('degree-form');
var workForm = document.getElementsByClassName('work-form');
var demodDetails = document.getElementsByClassName('demo-details');

window.onclick = function () {

    if (!event.target.matches('.navbar')) {



        for (var i = 0; i < document.getElementsByClassName('search_input').length; i++) {
            document.getElementsByClassName('search_input')[i].style.display = 'none';
        }




        var drop_down_list = document.getElementsByClassName('dropdownlist');
        for (var i = 0; i < drop_down_list.length; i++) {
            drop_down_list[i].style.display = 'none';
        }
         var drop_down_list1 = document.getElementsByClassName('dropdownlist1');
        for (var i = 0; i < drop_down_list1.length; i++) {
            drop_down_list1[i].style.display = 'none';
        }

    }
};
window.onload = function () {
    for (var i = 0; i < document.getElementsByClassName('comments').length; i++) {
        if (document.getElementsByClassName('comments')[i].clientHeight > 300 ) {
      console.log(true);
      document.getElementsByClassName('comments')[i].style.height = '300px';
      document.getElementsByClassName('more')[i].style.display = 'block';}}
};

function expand(a, b) {
    a.style.display = 'none';
    var el = document.getElementById(b);
    el.style.height = 'auto';

}
function openmenu() {
var navitem =document.getElementsByClassName('nav-item');
var iddrop =document.getElementById('drop');
var iddrop1 =document.getElementById('drop1');
var navform =document.getElementsByClassName('.navform');
for(var i = 0; i < navitem.length; i++){
       navitem[i].style.display= 'block';}
    iddrop.style.display= 'block';
    iddrop1.style.display= 'block';

for(var i = 0; i < navform.length; i++){
       navform[i].style.display= 'block';}


}

function revealsearchinput() {
    for(var i = 0; i < document.getElementsByClassName('search_input').length; i++){
       document.getElementsByClassName('search_input')[i].style.display= 'inline';}
}

function dropdownlist(a) {
    var drop_down_list =document.getElementsByClassName('dropdownlist');
    var myprof =document.getElementsByClassName('myprof');
    for(var i = 0; i < drop_down_list.length; i++) {
    drop_down_list[i].style.display = 'flex';}
    for(var i = 0; i < myprof.length; i++) {
    myprof[i].style.display = 'block';}

}
function dropdownlist1(a) {
    console.log('clicked');
    var drop_down_list =document.getElementsByClassName('dropdownlist1');
    for(var i = 0; i < drop_down_list.length; i++) {
    drop_down_list[i].style.display = 'flex';}
}
function showeditforms(){
    
    for(var i = 0; i < document.getElementsByClassName('contact-details').length; i++){
       document.getElementsByClassName('contact-details')[i].style.display= 'none';}
    for(var i = 0; i < document.getElementsByClassName('contact-details-form').length; i++){
       document.getElementsByClassName('contact-details-form')[i].style.display= 'inline';}
}

function addnewforms() {
    var link_form = document.getElementById('addlinkform');
    var para = document.createElement("P");
    var ine = document.createElement('Input');
    ine.type = 'text';
    ine.name= 'link_name';
    ine.placeholder= 'Add name of link';
    var paratext = document.createTextNode(" : ");
    var ine2 = document.createElement('Input');
    ine2.type = 'url';
    ine2.name= 'link';
    ine2.required=true;
    ine2.placeholder= 'Add url of link';
    para.appendChild(ine);
    para.appendChild(paratext);
    para.appendChild(ine2);
    link_form.appendChild(para);
}
function addnewlinkforms(x) {
    var link_form = document.getElementById(x);
    var para = document.createElement("P");
    var ine = document.createElement('Input');
    ine.type = 'text';
    ine.name= 'link_name';
    ine.placeholder= 'Add name of link';
    var paratext = document.createTextNode(" : ");
    var ine2 = document.createElement('Input');
    ine2.type = 'url';
    ine2.name= 'link';
    ine2.required=true;
    ine2.placeholder= 'Add url of link';
    para.appendChild(ine);
    para.appendChild(paratext);
    para.appendChild(ine2);
    link_form.appendChild(para);
}
function personalform() {
for(var i = 0; i < demodDetails.length; i++){
       demodDetails[i].style.display= 'none';}

for(var i = 0; i < personalForm.length; i++){
       personalForm[i].style.display= 'block';}
}

function degreeform() {


for(var i = 0; i < degreeForm.length; i++){
       degreeForm[i].style.display= 'block';}
}

function workform() {


for(var i = 0; i < workForm.length; i++){
       workForm[i].style.display= 'block';}
}

function addbookform () {

   
    var form = document.getElementsByClassName('create-book-form');
    for(var i = 0; i < form.length; i++){
       form[i].style.display= 'block';}
}
    
function editbookform () {
    var details = document.getElementsByClassName('subject-heading');
    for(var i = 0; i < details.length; i++){
       details[i].style.display= 'none';}
    var form = document.getElementsByClassName('edit-book-form');
    for(var i = 0; i < form.length; i++){
       form[i].style.display= 'block';}
}

function checkfilesize(a) {
    filefield= document.getElementById('filefield');
    console.log(filefield.files.length);
    if (filefield.files[0].size/1024/1024 > 5){
        alert('File size exceeds 5 MB');
    }
    else {

    }
}

function checkvalidity() {
    filefield=document.getElementById('filefield');

    console.log('worked');
    if (filefield.files[0].size/1024/1024 > 5){
        event.preventDefault();
        alert('File size exceeds 5 MB');
        return false;
    }
    else {
        return true;
    }
}
function bookdetails() {
    var details = document.getElementsByClassName('subject-heading');
    for(var i = 0; i < details.length; i++){
       details[i].style.display= 'none';}
    var subdetails = document.getElementsByClassName('subject-details-review');
    for(var i = 0; i < details.length; i++){
       subdetails[i].style.display= 'block';}
}


function removebook(x) {
    var message = confirm('Are you sure you want to delete the book');
    if (message==true){
        window.location.href = x;
        console.log(true);
    }
    else{
        console.log(false);
    }
}
function removereview(x) {
    var message = confirm('Are you sure you want to delete the review');
    if (message==true){
        window.location.href = x;
        console.log(true);
    }
    else{
        console.log(false);
    }
}

function deletepost(x) {
    var message = confirm('Are you sure you want to delete the post');
    if (message==true){
        window.location.href = x;
        console.log(true);
    }
    else{
        console.log(false);
    }
}

function commentform(){
    var subdetails = document.getElementsByClassName('comment-create-form');
    for(var i = 0; i < subdetails.length; i++){
       subdetails[i].style.display= 'block';}
}

function editsubjectintro(action, heading, details) {
       document.getElementsByClassName('showsubjectintro')[0].style.display= 'none';
    document.getElementById('subject-intro-edit').style.display = 'block';
    console.log(action);
    document.getElementById('subject-intro-edit').action = action;
    document.getElementsByName('heading')[0].value = heading;
    document.getElementsByName('details')[0].value = details;
    

}
function addsubjectintro() {
   document.getElementById('subject-intro-add').style.display = 'block';
    
}
