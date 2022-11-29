const enterDistrictsTotalDistrictsInput = document.getElementById(
	"totalDistrictsInput"
);

const districtDataInputArea = document.getElementById("districtDataInputArea");

// let totalDistricts = 0;

let districts = [];

enterDistrictsTotalDistrictsInput.addEventListener("change", (event) => {
	// console.log(event.target.value);
	totalDistricts = event.target.value;
	updateNumOfDistrictDivs(Number(event.target.value));
});

const addDivs = (newTotal) => {
	for (let i = districts.length; i < newTotal; i++) {
		index = 0;
		if (districts.length > 0)
			index = Number(districtDataInputArea.lastChild.id) + 1;
		const choiceDiv = document.createElement("div");
		choiceDiv.id = index;
		// choiceDiv.className = "choice";
		// choiceDiv.style.display = "none";

		const choiceMessage = document.createElement("div");
		choiceMessage.innerText = "Hello" + index;
		choiceMessage.id = "message" + index;
		// choiceMessage.className = "message";
		choiceDiv.appendChild(choiceMessage);

		const choiceButton = document.createElement("button");
		choiceButton.id = "button" + index;
		choiceButton.innerText = "Remove District";
		// choiceButton.className = "button";
		choiceDiv.appendChild(choiceButton);

		choiceButton.addEventListener("click", () => {
			removeSelf(index, choiceDiv);
		});

		districtDataInputArea.appendChild(choiceDiv);

		districts.push(index);
	}
};

const removeDivs = (newTotal) => {
	for (let i = districts.length; i > newTotal; i--) {
		districtDataInputArea.removeChild(
			districtDataInputArea.lastElementChild
		);
		districts.pop();
	}
};

const removeSelf = (index, self) => {
	districts.splice(index, 1);
	districtDataInputArea.removeChild(self);
};

const updateNumOfDistrictDivs = (totalDistricts) => {
	if (districts.length < totalDistricts) addDivs(totalDistricts);
	else if (districts.length > totalDistricts) removeDivs(totalDistricts);
	// console.log(totalDistricts);
	// console.log(districts.length);
	console.log(districts);
};
