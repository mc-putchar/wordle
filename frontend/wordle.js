const WORD_LEN = 5;
const user_token = "blabla"
let currentRow = 0;
let currentCell = 0;

function onKeyClick() {
	if (currentCell < WORD_LEN) {
		const board = document.getElementById("gameboard");
		board.rows[currentRow].cells[currentCell].textContent = "[" + this.textContent + "]";
		++currentCell;
	}
}

function onDelete() {
	const board = document.getElementById("gameboard");
	if (currentCell) {
		--currentCell;
	}
	board.rows[currentRow].cells[currentCell].textContent = "[ ]";
}

function onSend() {
	let word = "";
	if (currentCell < WORD_LEN) {
		alert("Not enough letters.");
	} else {
		const board = document.getElementById("gameboard");
		for (let i = 0; i < WORD_LEN; ++i) {
			word += board.rows[currentRow].cells[i].textContent[1];
		}
		fetch("/word", {
			headers: {
				'Accept': 'application/json',
				'Content-Type': 'application/json'
			},
			method: "POST",
			body: JSON.stringify({token: user_token, attempt: word})
		}).then(res => console.log(res))
		.catch(res => console.log(res));
	}
}

class Keyboard {
	constructor() {
		this.element = document.createElement("table");
		this.keyrows = ["qwertyuiop1", "asdfghjkl 0", "zxcvbnm    "];
		this.keyrows.forEach(row => {
			const trow = document.createElement("tr");
			for (let i = 0; i < row.length; i++) {
				const col = document.createElement("tc");
				const btn = document.createElement("button");
				btn.className = "key";
				switch (row[i]) {
					case '0':
						btn.textContent = "⏎";
						btn.id = "enter";
						btn.addEventListener('click', onSend.bind(btn));
						break;
					case '1':
						btn.textContent = "←";
						btn.id = "backspace";
						btn.addEventListener('click', onDelete.bind(btn));
						break;
					case ' ':
						btn.className = "spacer";
						break;
					default:
						btn.textContent = row[i];
						btn.addEventListener('click', onKeyClick.bind(btn));
						break;
				}
				col.appendChild(btn);
				trow.appendChild(col);
			}
			this.element.appendChild(trow);
		});
	}
};

document.addEventListener("DOMContentLoaded", function() {
	const keyboard = new Keyboard();
	const page = document.getElementById("keyboard");
	page.appendChild(keyboard.element);
});
