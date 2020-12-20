
var male=document.getElementById('gn1');
var fem=document.getElementById('gn2');
var tik1=document.getElementById('tik1');
var tik2=document.getElementById('tik2');
var gender=document.getElementById('genders').getElementsByTagName('option');
// gender.setAttribute()
// male.setAttribute('value','fem')
// console.log(gender)

if (gender[0].selected){
    tik1.style.display='inline-block';
}else if(gender[1].selected){
    tik2.style.display='inline-block';
}
male.addEventListener('click',function(){
   
    tik1.style.display='inline-block';
    tik2.style.display='none';
    // console.log(gender[0])
    gender[0].selected=true
});
fem.addEventListener('click',function(){
       
        tik2.style.display='inline-block';
        tik1.style.display='none';
        console.log(gender[1].selected)
        gender[1].selected=true;
    });


