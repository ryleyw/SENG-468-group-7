import React, {useState} from 'react'
import axios from 'axios'

function SellButton(props) {
	const [amount, setAmount] = useState(0)
	const [pending, setPending] = useState(false)
	const [showModal, setShowModal] = useState(false)

	function sellStock(e) {
		e.preventDefault()
		const data = {
			'command': 'SELL',
			'stock': props.stock,
			'amount': amount,
			'userid': props.user
		}

		axios.post('http://localhost:81/', data).
			then((response) => {
				console.log(response.data)
				setPending(true)
			}, (error) => {
				alert(error)
			})
	}

	function changeAmount(e) {
		setAmount(e.target.value)
	}

	function commitSell() {
		const data = {
		    'command': 'COMMIT_SELL',
		    'userid': props.user
		}
		axios.post('http://localhost:81/', data).
		    then((response) => {
		        console.log(response.data)
		        setPending(false)
		        setShowModal(false)
		        props.setInfo(response.data.result)
		    }, (error) => {
		        alert(error)
		    })
    	}

	function cancelSell() {
		const data = {
			'command': 'CANCEL_SELL',
			'userid': props.user
		}
		axios.post('http://localhost:81/', data).
			then((response) => {
				console.log(response.data)
				setPending(false)
				setShowModal(false)
			}, (error) => {
				alert(error)
			})
    	}
		

	const modal = (
		<div className="modal">
		    <button onClick={() => setShowModal(false)}>close</button>
		    <div>        
			<div>
				<form onSubmit={sellStock}>
				<input type="number" onChange={changeAmount} value={amount} placeholder="enter amount..."></input>
						<input type="submit" className="addButton" value="Sell Amount"></input>
					</form>
				</div>
			<div>
		            {pending &&
		                <div> 
					<button onClick={commitSell}>Confirm</button>
					<button onClick={cancelSell}>Cancel</button>
				</div>
		            }
		    	</div>

		    </div>
		</div>
    	);

	return (
		<div>
			<button onClick={()=>setShowModal(true)}>SELL</button>
			{showModal && <div>{modal}</div>}
		</div>
	)
}

export default SellButton
