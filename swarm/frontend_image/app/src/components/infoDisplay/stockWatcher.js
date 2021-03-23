import React, {useState, useEffect} from 'react'
import axios from 'axios'


// This div takes a stock as prop and fetches the quote on render
//ideally would use a hook but i dont think its necessary for this assignment

function StockWatcher(props) {
    const [stock, setStock] = (props.stock)
    const [quote, setQuote] = useState(null)
    const [loading, setLoading] = useState(false)
    //useeffect to get stock and set quote price

    useEffect(() => {

    	const data = {
		'command': 'QUOTE',
		'stock': props.stock,
		'userid': props.user
	}

	axios.post('http://localhost:81/', data).
		then((response) => {
			console.log(response.data)
			setQuote(response.data.result.price)
		}, (error) => {
			alert(error)
		})
    }, []);

    return (
        <div>
        {quote!=null && 
            <div className="stockWatcher">
		{quote}
            </div>
        }
        </div>
    )
}

export default StockWatcher
