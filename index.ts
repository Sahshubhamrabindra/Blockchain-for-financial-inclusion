import express from 'express';
import * as crypto from 'crypto';

class Transaction {
  constructor(
    public amount: number,
    public payer: string,
    public payee: string
  ) {}

  toString() {
    return JSON.stringify(this);
  }
}

class Block {
  public nonce = Math.round(Math.random() * 999999999);

  constructor(
    public prevHash: string,
    public transaction: Transaction,
    public ts = Date.now()
  ) {}

  get hash() {
    const str = JSON.stringify(this);
    const hash = crypto.createHash('SHA256');
    hash.update(str).end();
    return hash.digest('hex');
  }
}

class Chain {
  public static instance = new Chain();

  chain: Block[];

  constructor() {
    this.chain = [
      new Block('', new Transaction(0, 'genesis', 'A'))
    ];
  }

  get lastBlock() {
    return this.chain[this.chain.length - 1];
  }

  mine(nonce: number) {
    let solution = 1;
    console.log('⛏️  mining...');

    while (true) {
      const hash = crypto.createHash('MD5');
      hash.update((nonce + solution).toString()).end();

      const attempt = hash.digest('hex');

      if (attempt.substr(0, 4) === '0000') {
        console.log(`Solved: ${solution}`);
        return solution;
      }

      solution += 1;
    }
  }

  addBlock(transaction: Transaction, senderPublicKey: string, signature: Buffer) {
    const verify = crypto.createVerify('SHA256');
    verify.update(transaction.toString());

    const isValid = verify.verify(senderPublicKey, signature);

    if (isValid) {
      const newBlock = new Block(this.lastBlock.hash, transaction);
      newBlock.nonce = this.mine(newBlock.nonce);

      const beforeBalance = this.getBalance(transaction.payee);

      if (transaction.amount <= beforeBalance) {
        console.log(`Before balance (before received): ${beforeBalance}`);
        this.chain.push(newBlock);

        const afterBalance = this.getBalance(transaction.payee);
        console.log(`After balance (after received): ${afterBalance}`);
        console.log(`Transaction successful. Deducted ${transaction.amount} from ${transaction.payer}'s account.`);
      } else {
        console.log('Transaction unsuccessful. Insufficient funds.');
        console.log(`Before balance (before deduction): ${beforeBalance}`);
      }
      
    } else {
      console.log('Transaction unsuccessful. Invalid signature.');
    }
  }

  getBalance(publicKey: string): number {
    let balance = 1000;

    for (const block of this.chain) {
      if (block.transaction.payee === publicKey) {
        balance += block.transaction.amount;
      }
      if (block.transaction.payer === publicKey) {
        balance -= block.transaction.amount;
      }
    }

    return balance;
  }
}

class Wallet {
  public publicKey: string;
  public privateKey: string;

  constructor() {
    const keypair = crypto.generateKeyPairSync('rsa', {
      modulusLength: 2048,
      publicKeyEncoding: { type: 'spki', format: 'pem' },
      privateKeyEncoding: { type: 'pkcs8', format: 'pem' },
    });

    this.privateKey = keypair.privateKey;
    this.publicKey = keypair.publicKey;
  }

  sendMoney(amount: number, payeePublicKey: string) {
    const transaction = new Transaction(amount, this.publicKey, payeePublicKey);

    const sign = crypto.createSign('SHA256');
    sign.update(transaction.toString()).end();

    const signature = sign.sign(this.privateKey);
    Chain.instance.addBlock(transaction, this.publicKey, signature);
  }
}

const app = express();
const port = 3000;

app.use(express.static('public'));

app.post('/sendMoney', express.json(), (req, res) => {
  const { amount, payerprivateKey, payeePublicKey } = req.body;

  const senderWallet = new Wallet();
  const parsedAmount = parseFloat(amount);
  const transaction = new Transaction(parsedAmount, payerprivateKey, payeePublicKey);
  const sign = crypto.createSign('SHA256');
  sign.update(transaction.toString()).end();
  const signature = sign.sign(senderWallet.privateKey);
  Chain.instance.addBlock(transaction, senderWallet.publicKey, signature);

  res.json({
    success: true,
    message: 'Transaction successful',
    chain: Chain.instance.chain,
  });
});

app.listen(port, () => {
  console.log(`Server is running at http://localhost:${port}`);
});

// Example usage
const A = new Wallet();
const B = new Wallet();
const C = new Wallet();

// A.sendMoney(100, C.publicKey);
// B.sendMoney(50, A.publicKey);
// C.sendMoney(75, B.publicKey);
// B.sendMoney(20, C.publicKey);

console.log(Chain.instance);
