import React, {useState} from 'react'
import axios from 'axios'
import StockWatcher from './stockWatcher'
import CancelButton from './cancelButton'
//BUGS:
//after sell row above takes on the quote price
//bought at is total cose - divide by number of stocks.
//make refresh button

function MyTriggers(props) {
    
    const [showModal, setShowModal] = useState(false)
    const [stock, setStock] = useState("")
    const [quote, setQuote] = useState(null)
    const [amount, setAmount] = useState(0)
    const [pending, setPending] = useState(false)
    const [sell, setSell] = useState(false)

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

    function addBuyTrigger(e) {
	    e.preventDefault()
        console.log(stock)
        console.log(amount)
    }

    function addSellTrigger(e) {
        e.preventDefault()
        console.log(stock)
        console.log(amount)
    }

    function commitBuyTrigger() {
        console.log("confirm buy trigger")
    }

    function commitSellTrigger() {
        console.log("confirm sell trigger")
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
		        {props.info.stocks[element].cost}
		    </div>
		    <div className="entry">
		        {props.info.stocks[element].units}
		    </div>
		    <div className="entry">
		        <StockWatcher user={props.user} stock={element} />
		    </div>
		    <div className="entry">
		        <CancelButton user={props.user} stock={element} setInfo={props.setInfo} mode={sell}/>
		    </div>
		</div>
    	)
    }

    console.log(sell)
    const modal = (
        <div className="modal">
            <button onClick={() => setShowModal(false)}>close</button>
            <div>
            Enter trigger to set:
                {setSell ?
                <button onClick={()=>setSell(false)}>
                    BUY TRIGGER
                </button>
                :
                <button style={{fontWeight: 'bold'}} onClick={()=>setSell(false)}>
                    BUY TRIGGER
                </button>
                }
                {setSell?
                <button style={{fontWeight: 'bold'}} onClick={()=>setSell(true)}>
                    SELL TRIGGER
                </button>
                :
                <button onClick={()=>setSell(true)}>
                    SELL TRIGGER
                </button>
                }
                {sell?
                <form onSubmit={QuoteStock}>
                    <select onChange={changeStock} value={stock}>
                        {Object.keys(props.info.stocks).map((element, index) => 
                            <option value={element}>{element}</option>
                        )}
                    </select>
                    <input type="submit" className="addButton" value="Get Quote"></input>
                </form>
                :
                <form onSubmit={QuoteStock}>
                    <input type="text" onChange={changeStock} value={stock} placeholder="eg. ESN"></input>
                    <input type="submit" className="addButton" value="Get Quote"></input>
                </form>
                }
                {quote!=null &&
			    <div>
                    {sell ?
                    <div>
                        <div>Sell Trigger Amount: {quote}</div>
                        <form onSubmit={addBuyTrigger}>
                            <input type="number" onChange={changeAmount} value={amount} placeholder="enter amount..."></input>
                            <input type="submit" className="addButton" value="Buy Amount"></input>
                        </form>
                    </div>
                    :
                    <div>
                        <div>Buy Trigger Amount: {quote}</div>
                        <form onSubmit={addSellTrigger}>
                            <input type="number" onChange={changeAmount} value={amount} placeholder="enter amount..."></input>
                            <input type="submit" className="addButton" value="Buy Amount"></input>
                        </form>
                    </div>
                    }
                	
			    </div>
                }
		    <div>
                {pending &&
                    <div> 
                        {sell? 
                            <button onClick={commitSellTrigger}>CONFIRM SELL TRIGGER</button>
                            :
                            <button onClick={commitBuyTrigger}>CONFIRM BUY TRIGGER</button>
                        }
			        </div>
                }
            </div>
        </div>
    </div>
    );

    return (
        <div className="myStocksContainer">
            <button onClick = {()=> setShowModal(true)}>Create Triggers</button>
            {showModal && <div>{modal}</div>}
            <div className="entryContainer">
                <div className="entry">
                    STOCK
                </div>
                <div className="entry">
                    TRIGGER
                </div>
                <div className="entry">
                    TRIGGER AMOUNT
                </div>
                <div className="entry">
                    TRIGGER PRICE
                </div>
                <div className="entry">
                    CANCEL?
                </div>
            </div>
            {stockList}
        </div>
    )
}

export default MyTriggers