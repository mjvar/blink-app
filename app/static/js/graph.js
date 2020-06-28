//initializing global array holding data
var newValues = [];
var last;
var to_add = 0

 //returns last value in array, called in updateData()
var lastOne =  function(array) {
if (array == null) 
	return void 0;
else
	return array[array.length - 1];  
}

function processFile(){
	var file = document.querySelector('#myFile').files[0]; //still need to figure out how to do this w/o user input
	var reader = new FileReader()
	reader.readAsText(file)
  
	//When the file finish load
	reader.onload = function(event) {
  
	  //get the file
	  var csv = event.target.result
	
	  //split and get the rows in an array
	  var rows = csv.split('\n')
  
	  //move line by line
	  for (var i = 1; i < rows.length; i++) {
		//split by separator (,) and get the columns
		cols = rows[i].split(',')
		last = parseInt(cols[1], 10)
		newValues.push(last)
	  }
	  updateData(lastOne(newValues))
	}
  }

const interval = setInterval(function() {
   // method to be executed;
   processFile()
 }, 2000);

// Chart set up
var ctx = document.getElementById('myChart').getContext('2d');
var chart = new Chart(ctx, {
    // The type of chart we want to create
    type: 'line',

    // The data for our dataset
    data: {
        labels: ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
        datasets: [{
            label: 'Your Drowsiness Data',
            backgroundColor: 'rgb(2, 111, 164)',
            borderColor: 'rgb(226, 150, 148)',
            data: []
        }]
    },

    // Configuration options go here
    options: {
    	legend: {
    		labels: {
    			fontColor: "rgb(255, 255, 255)",
    		}
    	},
    	scales: {
            xAxes: [{
            	gridLines: { 
            		color: "#dddddd" 
            	},
            	ticks: {
            		fontColor: "#dddddd"
            	}
            }],
            yAxes: [{
            	gridLines: { 
            		color: "#dddddd" 
            	},
            	ticks: {
            		fontColor: "#dddddd"
            	}
            }]
        }

    }
});

// Function to update data
// Backend should find a way to call this function or execute code in it
function updateData() {
	const response = fetch('http://localhost:5000/eye_data')
  .then(response => response.json())  
  .then(json => (to_add = json.score))	// Maximum data entries we will be working with
  	console.log(to_add)
	const MAX_DATA = 40
	var length = chart.data.datasets[0].data.length
	// If there are as many entries as we intend on using, shift existing ones
	if(length == MAX_DATA) {
		for(var i = 1; i < length; i++) {
			chart.data.datasets[0].data[i - 1] = chart.data.datasets[0].data[i]
		}
		chart.data.datasets[0].data[length - 1] = to_add
	}
	// Else push in new data element
	else {
		chart.data.datasets[0].data.push(to_add)
	}
	// chart.data.datasets[0].data[chart.data.datasets[0].data.length - 1] = lastOne(newValues)
	chart.data.datasets[0].data[chart.data.datasets[0].data.length - 1] = to_add

	chart.update()
	setTimeout(updateData, 1000);
}

// Function in charge of changing page. It will hide all pages but the one selected in hamburger menu
// Called directly by the navbar
function hide(selected) {
	var options = document.getElementsByClassName("options")
	var buttons = document.getElementsByClassName("menu-buttons")
	for(var i = 0; i < options.length; i++) {
		options[i].classList.add("hidden")
		buttons[i].classList.remove("active")
	}
	// console.log(3)
	options[selected].classList.remove("hidden")
	buttons[selected].classList.add("active")
}



// These 2 functions make the text input work
// They will be removed later
function getData() {
	var searchBox = document.getElementById("input")
	updateData()
	searchBox.value = ""
}

document.addEventListener('keypress', function (e) {
	if (e.key === 'Enter') {
		// code for enter
  		getData()
	}
});

setTimeout(updateData, 1000);