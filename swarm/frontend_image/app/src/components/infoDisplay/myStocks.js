import React, {useState} from 'react'
import axios from 'axios'

function MyStocks(props) {

    const [showModal, setShowModal] = useState(false)
    const [stock, setStock] = useState("")
    const [quote, setQuote] = useState(null)

    function QuoteStock(e) {
        e.preventDefault()
    }

    function changeStock(e) {
        setStock(e.target.value)
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
                    <div>Stock result</div>
                }
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