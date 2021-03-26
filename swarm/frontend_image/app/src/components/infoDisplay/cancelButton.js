import React, {useState} from 'react'
import axios from 'axios'

function CancelButton(props) {
    
	const [showModal, setShowModal] = useState(false)

    function cancelBuyTrigger() {
        const data = {
            'command': 'CANCEL_SET_BUY',
            'stock': props.stock,
            'userid': props.user
        }

        axios.post('http://localhost:81/', data).
		    then((response) => {
		        console.log(response.data)
		        setShowModal(false)
		        props.setInfo(response.data.result)
		    }, (error) => {
		        alert(error)
		    })
    }
    

    function cancelSellTrigger() {
        const data = {
            'command': 'CANCEL_SET_SELL',
            'stock': props.stock,
            'userid': props.user
        }

        axios.post('http://localhost:81/', data).
		    then((response) => {
		        console.log(response.data)
		        setShowModal(false)
		        props.setInfo(response.data.result)
		    }, (error) => {
		        alert(error)
		    })
    }

	return (
		<div>
            {props.mode?
            (<button onClick={()=>cancelSellTrigger()}>
                CANCEL
            </button>)
            :
            (<button onClick={()=>cancelBuyTrigger()}>
                CANCEL
            </button>)}
		</div>
	)
}

export default CancelButton
