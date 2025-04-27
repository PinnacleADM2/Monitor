        import logging
        from cryptofeed import FeedHandler
        from cryptofeed.exchanges import Binance, Bybit, Bitfinex, Coinbase, OKX, Kraken, Bitmex, Huobi, Kucoin, Gateio, Poloniex # Adicione ou remova exchanges conforme necessário
        from cryptofeed.defines import TRADES, L2_BOOK, FUNDING, LIQUIDATIONS, OPEN_INTEREST
        from cryptofeed.backends.postgres import TradePostgres, BookPostgres, FundingPostgres, LiquidationPostgres, OpenInterestPostgres

        # --- IMPORTANTE: CONFIGURE SUAS CREDENCIAIS AQUI ---
        POSTGRES_CONFIG = {
            'host': 104.248.229.162,  # <-- Substitua! Use o IP público do servidor OU 'localhost' se o banco e o app rodam NO MESMO servidor.
            'port': 5432,
            'user': Pinnacle,        # <-- Substitua pelo seu usuário do banco
            'password': Pinnacle881126, # <-- Substitua pela sua senha do banco
            'database': pinnaclemonitor       # <-- Substitua pelo nome do seu banco
        }
        # -----------------------------------------------------

        # Configura o logging para ver mensagens do cryptofeed
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)

        def main():
            logger.info("Iniciando FeedHandler...")
            fh = FeedHandler()

            # Lista das exchanges que você quer conectar
            exchanges_to_run = [
                Binance, Bybit, Bitfinex, Coinbase, OKX, Kraken, Bitmex, Huobi, Kucoin, Gateio, Poloniex,
                # Adicione outras classes de Exchange aqui se precisar
            ]

            # Lista de canais que você quer para TODAS as exchanges (verifique se a exchange suporta!)
            channels_to_subscribe = [TRADES, L2_BOOK, FUNDING, LIQUIDATIONS, OPEN_INTEREST]

            # Adiciona cada exchange ao FeedHandler
            for exchange_class in exchanges_to_run:
                try:
                    # Define os callbacks para cada tipo de dado, usando a config do Postgres
                    callbacks = {
                        TRADES: TradePostgres(**POSTGRES_CONFIG),
                        L2_BOOK: BookPostgres(**POSTGRES_CONFIG),
                        FUNDING: FundingPostgres(**POSTGRES_CONFIG),
                        LIQUIDATIONS: LiquidationPostgres(**POSTGRES_CONFIG),
                        OPEN_INTEREST: OpenInterestPostgres(**POSTGRES_CONFIG),
                    }

                    # Cria a instância da exchange e adiciona ao feed handler
                    # Nota: Nem toda exchange suporta todos os canais. Cryptofeed tentará conectar aos que ela suporta.
                    fh.add_feed(exchange_class(
                        channels=channels_to_subscribe,
                        callbacks=callbacks
                        # Você pode adicionar 'symbols' aqui se quiser apenas pares específicos, ex: symbols=['BTC-USDT', 'ETH-USDT']
                    ))
                    logger.info(f"Adicionada feed para {exchange_class.__name__}")

                except Exception as e:
                    logger.error(f"Erro ao adicionar feed para {exchange_class.__name__}: {e}")

            logger.info("Iniciando a execução do FeedHandler (fh.run())...")
            fh.run()
            logger.info("FeedHandler encerrado.") # Esta linha só será alcançada se fh.run() parar

        if __name__ == '__main__':
            main()