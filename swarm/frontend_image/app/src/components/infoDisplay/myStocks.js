import React, {useState} from 'react'
import axios from 'axios'
import StockWatcher from './stockWatcher'
import SellButton from './sellButton'

//BUGS:
//after sell row above takes on the quote price
//bought at is total cose - divide by number of stocks.
//make refresh button

function MyStocks(props) {

    const [showModal, setShowModal] = useState(false)
    const [stock, setStock] = useState("")
    const [quote, setQuote] = useState(null)
    const [amount, setAmount] = useState(0)
    const [pending, setPending] = useState(false)

    const fakeData ={
        "MSF": {
            "cost": 200.20,
            "units": 2
        },
        "AMZ": {
            "cost": 10.85,
            "units": 6
        },
        "LZR": {
            "cost": 52.21,
            "units": 3
        }
    }

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
    
    
    var stockList = null

    if (props.info != null) {
	stockList = Object.keys(props.info.stocks).map((element, index) => 
		<div className="entryContainer" key={index}>
		    <div className="entry">
		        {element}
		    </div>
		    <div className="entry">
		        {(props.info.stocks[element].cost/props.info.stocks[element].units).toFixed(2)}
		    </div>
		    <div className="entry">
		        {props.info.stocks[element].units}
		    </div>
		    <div className="entry">
		        <StockWatcher user={props.user} stock={element} />
		    </div>
		    <div className="entry">
		        <SellButton user={props.user} stock={element} setInfo={props.setInfo}/>
		    </div>
		</div>
    	)
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
            <div className="entryContainer">
                <div className="entry">
                    STOCK
                </div>
                <div className="entry">
                    BOUGHT AT
                </div>
                <div className="entry">
                    UNITS OWNED
                </div>
                <div className="entry">
                    CURRENT PRICE
                </div>
                <div className="entry">
                    SELL?
                </div>
            </div>
            {stockList}
        </div>
    )
}

export default MyStocks
