import React, {useState} from 'react'
import axios from 'axios'


// This div takes a stock as prop and fetches the quote on render
//ideally would use a hook but i dont think its necessary for this assignment

function StockWatcher(props) {
    const [stock, setStock] = (props.stock)
    const [quote, setQuote] = useState(null)
    const [loading, setLoading] = useState(false)
    //useeffect to get stock and set quote price

    return (
        <div>
        {loading && 
            <div className="stockWatcher">
                Quote Price
            </div>
        }
        </div>
    )
}