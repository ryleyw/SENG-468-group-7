import React, {useState} from 'react'
import axios from 'axios'

function MyStocks(props) {

    const [showModal, setShowModal] = useState(false)
    const [stock, setStock] = useState("")
    const [quote, setQuote] = useState(null)
    const [amount, setAmount] = useState(0)
    const [pending, setPending] = useState(false)

    function QuoteStock(e) {
        e.preventDefault()
	const data = {
		'command': 'QUOTE',
		'stock': stock,
		'userid': props.user
	}

	axios.post('http://localhost:81/', data).
		then((response) => {
			console.log(response.data)
			setQuote(response.data.result.price)
		}, (error) => {
			alert(error)
		})
    }

    function buyStock(e) {
	e.preventDefault()
	const data = {
		'command': 'BUY',
		'stock': stock,
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

    function commitBuy() {
	const data = {
		'command': 'COMMIT_BUY',
		'userid': props.user
	}
	axios.post('http://localhost:81/', data).
		then((response) => {
			console.log(response.data)
			setPending(false)
			setQuote(null)
			setShowModal(false)
			props.setInfo(response.data.result)
		}, (error) => {
			alert(error)
		})
    }

    function cancelBuy() {
	const data = {
		'command': 'CANCEL_BUY',
		'userid': props.user
	}
	axios.post('http://localhost:81/', data).
		then((response) => {
			console.log(response.data)
			setPending(false)
			setQuote(null)
			setShowModal(false)
		}, (error) => {
			alert(error)
		})
    }


    function changeStock(e) {
        setStock(e.target.value)
    }

    function changeAmount(e) {
	setAmount(e.target.value)
    }

    

    const modal = (
        <div className="modal">
            <button onClick={() => setShowModal(false)}>close</button>
            <div>
            Enter stock to buy:
                <form onSubmit={QuoteStock}>
                    <input type="text" onChange={changeStock} value={stock} placeholder="eg. ESN"></input>
                    <input type="submit" className="addButton" value="Get Quote"></input>
                </form>
                {quote!=null &&
			<div>
                		<div>Stock Price: {quote}</div>
				<form onSubmit={buyStock}>
					<input type="number" onChange={changeAmount} value={amount} placeholder="enter amount..."></input>
					<input type="submit" className="addButton" value="Buy Amount"></input>
				</form>
			</div>
                }
		<div>
                    {pending &&
                        <div> 
				<button onClick={commitBuy}>Confirm</button>
				<button onClick={cancelBuy}>Cancel</button>
			</div>
                    }
            	</div>

            </div>
        </div>
    );

    return (
        <div className="myStocksContainer">
            <button onClick = {()=> setShowModal(true)}>Buy Stocks</button>
            {showModal && <div>{modal}</div>}
        </div>
    )
}

export default MyStocks
