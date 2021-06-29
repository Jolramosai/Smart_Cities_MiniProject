
function initialize_firebase(){
    var firebaseConfig = {
        apiKey: "AIzaSyABfWfSD_fUGUynRtvZYbY0avtUYbY9eR4",
        authDomain: "ozone-a07ef.firebaseapp.com",
        databaseURL: "https://ozone-a07ef.firebaseio.com",
        projectId: "ozone-a07ef",
        storageBucket: "ozone-a07ef.appspot.com",
        messagingSenderId: "1065032365783",
        appId: "1:1065032365783:web:f47ad75a461e01c7d36292",
        measurementId: "G-EEH0WTZ3G8"
    };
    // Initialize Firebase
    firebase.initializeApp(firebaseConfig);
    firebase.analytics();
}


function get_statistics(){
    var statisticsRef = firebase.database().ref('statistics');
    statisticsRef.on('value', function(snapshot) {
    snapshot.forEach(function(childSnapshot) {
      var childData = childSnapshot.val();
      statistics = childData
    });
});
}


function get_values(dict_key){
    dict = {}

    if(statistics == null) return

    console.log(statistics)
    for(x in statistics[dict_key]){
        y = statistics[dict_key][x].map(parseFloat)
        dict[x] = y
    }

    return dict
}

function get_collumns(collumn){

    if(statistics == null) return
    
    values = statistics[collumn]

    data = { 
        name: collumn, 
        hatchPalette: true, 
        defaultPoint_hatch_color: '#000', 
        palette: 'default', 
        
      } 
    
      points = []
      for(x in values){
          dict = {}
          dict["name"] = x
          dict["y"] = parseFloat(values[x])
          points.push(dict)
      }

      data["points"] = points
      
      console.log(data)

      return data

}

function get_last30days(){
    data = []
    last30days =  get_values("last30days")

    for(x in last30days){
        dict = {}
        dict["name"] = x
        arr = []
        values = last30days[x]
        for(var i = 0; i < values.length;i++){
            arr.push([i,values[i]])
        }
        dict["points"] = arr
        data.push(dict)
    }
    console.log(data)
    return data
}

function get_ngrams(){
    return get_collumns("ngrams")
}

function get_pollution(){
    return get_collumns("pollution")
}

function get_variations(){
    return get_collumns("variations")
}

function get_variations_city(city){
    if(statistics == null) return  

    return parseFloat(statistics["variations"][city]).toPrecision(4)
}


function get_pollution_city(city){
    if(statistics == null) return  

    return parseFloat(statistics["pollution"][city]).toPrecision(4)
}

function get_city_data(city){
    
    last30days = get_last30days()
    ngrams = get_ngrams()
    variations = get_variations()
    pollution = get_pollution()
    
    city_pollution = get_pollution_city(city)
    city_variation = get_variations_city(city)

    document.getElementById('initial').style.display = 'none'
    document.getElementById('statistics').style.display = 'flex'
    document.getElementById('charts1').style.display = 'flex'
    document.getElementById('charts2').style.display = 'flex'

    document.getElementById('ug_value').textContent = city_pollution
    document.getElementById('abs_value').textContent = city_variation
    document.getElementById('city_value').textContent = city
    console.log(city)
    
    JSC.Chart('pollution_chart',{
        title_label_text: 'Níveis de ozono em ug durante os ultimos 30 dias', 
        defaultSeries: { 
            type: 'line', 
            defaultPoint_marker_visible: false, 
            lastPoint: {  
              yAxisTick: { 
                axisId: 'secondY', 
                label_text: '%yValue'
              } 
            } 
          }, 
        series: last30days,
        options:{
            title:{
                display: true,
                text: "Níveis de ozono durante os ultimos 30 dias em ug"
            }
        }
    })

    var chart = JSC.chart('ngrams_chart', { 
        debug: true, 
        defaultSeries_type: 'column', 
        title_label_text: 'Ocorrencias dos ngrams mais frequentes de hoje', 
        series: [ngrams]
      }); 

      var chart = JSC.chart('ozone_chart', { 
        debug: true, 
        defaultSeries_type: 'column', 
        title_label_text: 'Niveis de ozono previstos nas diferentes localidades', 
        series: [pollution]
      }); 


      var chart = JSC.chart('variation_chart', { 
        debug: true, 
        defaultSeries_type: 'column', 
        title_label_text: 'Variações nos niveis de ozono previstas nas diferentes localidades', 
        series: [variations]
      }); 



}

function go_to_initial_page(){
    
    document.getElementById('initial').style.display = 'flex'
    document.getElementById('statistics').style.display = 'none'
    document.getElementById('charts1').style.display = 'none'
    document.getElementById('charts2').style.display = 'none' 
}

function getInputValue(id){
    var value = document.getElementById(id).value
    document.getElementById(id).value = ""
    return value;
}

function submitContact(e){
    e.preventDefault()
    var name = getInputValue("contactName")
    var email = getInputValue("contactEmail")
    saveMessage(name,email)
}

function saveMessage(name,email){
    var messagesRef = firebase.database().ref('contacts');
    var newMessageRef = messagesRef.push();
    newMessageRef.set({
        name: name,
        email: email
    })
}

initialize_firebase();
statistics = null
get_statistics()
document.getElementById('contact').addEventListener('submit',submitContact);